import uuid
from datetime import datetime, timezone
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.auth import get_current_user
from app.models.user import User
from app.models.challenge import Challenge, ChallengeTest
from app.models.submission import Submission, SubmissionResult
from app.models.progress import UserProgress
from app.schemas.submission import SubmissionCreate, SubmissionResponse
from app.api.executions import extract_function_name
from app.execution.executor import run_in_sandbox
from app.core.config import settings

router = APIRouter(tags=["submissions"])

def format_submission_response(submission: Submission, db: Session) -> dict:
    """Helper to dynamically filter and mask hidden test case results from response payloads."""
    tests = db.query(ChallengeTest).filter(ChallengeTest.challenge_id == submission.challenge_id).all()
    test_visibility = {t.id: t.visibility for t in tests}
    
    result_list = []
    for r in submission.results:
        visibility = test_visibility.get(r.test_id, "PUBLIC")
        if visibility == "HIDDEN":
            result_list.append({
                "id": r.id,
                "submission_id": r.submission_id,
                "test_id": r.test_id,
                "status": r.status,
                "runtime_ms": r.runtime_ms,
                "actual_output": None,  # Mask hidden test case output
                "error_type": r.error_type if r.status == "error" else None,
                "error_message": "Hidden test case output is hidden." if r.status != "passed" else None
            })
        else:
            result_list.append({
                "id": r.id,
                "submission_id": r.submission_id,
                "test_id": r.test_id,
                "status": r.status,
                "runtime_ms": r.runtime_ms,
                "actual_output": r.actual_output,
                "error_type": r.error_type,
                "error_message": r.error_message
            })
            
    return {
        "id": submission.id,
        "user_id": submission.user_id,
        "challenge_id": submission.challenge_id,
        "code": submission.code,
        "language": submission.language,
        "status": submission.status,
        "created_at": submission.created_at,
        "passed_tests": submission.passed_tests,
        "total_tests": submission.total_tests,
        "score": submission.score,
        "runtime_ms": submission.runtime_ms,
        "memory_bytes": submission.memory_bytes,
        "stdout": submission.stdout,
        "stderr": submission.stderr,
        "results": result_list
    }

@router.post("/submissions", response_model=SubmissionResponse)
def submit_code(
    req: SubmissionCreate,
    challenge_slug: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Validate challenge slug exists and is active
    challenge = db.query(Challenge).filter(
        Challenge.slug == challenge_slug,
        Challenge.status == "active"
    ).first()
    if not challenge:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Challenge not found"
        )
        
    # Validate code size limit
    code_bytes = len(req.code.encode("utf-8"))
    if code_bytes > settings.MAX_CODE_SIZE_BYTES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Code size exceeds limit of {settings.MAX_CODE_SIZE_BYTES} bytes."
        )

    # Validate rate limiting (maximum 2 concurrent runs per user)
    running_subs = db.query(Submission).filter(
        Submission.user_id == current_user.id,
        Submission.status.in_(["Pending", "Running"])
    ).count()
    if running_subs >= 2:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many concurrent runs. Please wait before submitting another job."
        )

    # Initialize submission record
    submission = Submission(
        user_id=current_user.id,
        challenge_id=challenge.id,
        code=req.code,
        language=req.language,
        status="Running",
        created_at=datetime.now(timezone.utc),
        passed_tests=0,
        total_tests=0,
        score=0.0
    )
    db.add(submission)
    db.commit()
    db.refresh(submission)

    # Fetch ALL tests (both public and hidden)
    all_tests = db.query(ChallengeTest).filter(ChallengeTest.challenge_id == challenge.id).all()
    submission.total_tests = len(all_tests)

    try:
        # Extract target function name
        func_name = extract_function_name(challenge.starter_code, challenge.slug.replace("-", "_"))
        
        # Format tests array
        test_cases_list = [
            {
                "id": str(t.id),
                "input_data": t.input_data,
                "expected_output": t.expected_output,
                "evaluation_type": t.evaluation_type or challenge.evaluation_type or "EXACT",
                "tolerance": t.tolerance or 1e-4,
                "metric": t.metric,
                "threshold": t.threshold
            }
            for t in all_tests
        ]

        # Run within isolated docker sandbox
        result = run_in_sandbox(req.code, req.language, func_name, test_cases_list)

        # Parse test outcomes
        sandbox_status = result["status"]
        submission.stdout = result.get("stdout", "")
        submission.stderr = result.get("stderr", "")
        submission.runtime_ms = result.get("runtime_ms", 0)
        submission.memory_bytes = 14 * 1024 * 1024 # Mock L2 memory execution standard

        passed_count = 0
        has_error = False
        has_fail = False

        for tc_res in result.get("tests", []):
            tc_id = uuid.UUID(tc_res["id"])
            tc_status = tc_res["status"]
            tc_actual = tc_res.get("actual")
            tc_error = tc_res.get("error")

            db_res = SubmissionResult(
                submission_id=submission.id,
                test_id=tc_id,
                status=tc_status,
                runtime_ms=result.get("runtime_ms", 0) // len(all_tests) if len(all_tests) > 0 else 0,
                actual_output=str(tc_actual) if tc_actual is not None else None,
                error_message=tc_error
            )
            
            if tc_status == "passed":
                passed_count += 1
            elif tc_status == "error":
                has_error = True
                db_res.error_type = "RuntimeError"
            else:
                has_fail = True

            db.add(db_res)

        submission.passed_tests = passed_count
        if len(all_tests) > 0:
            submission.score = float(passed_count) / float(len(all_tests))

        # Map statuses
        if sandbox_status == "TIMEOUT":
            submission.status = "TIME_LIMIT_EXCEEDED"
            submission.stderr = result.get("stderr", "Execution timed out.")
        elif sandbox_status == "FAILED" and not result.get("tests"):
            # SyntaxError or load failure
            submission.status = "COMPILATION_ERROR"
            submission.stderr = result.get("stderr", "Compilation/Syntax error.")
        elif has_error:
            submission.status = "RUNTIME_ERROR"
        elif has_fail:
            submission.status = "WRONG_ANSWER"
        else:
            submission.status = "ACCEPTED"
            
            # Update user challenge completion progress
            progress = db.query(UserProgress).filter(
                UserProgress.user_id == current_user.id,
                UserProgress.challenge_id == challenge.id
            ).first()
            if not progress:
                progress = UserProgress(
                    user_id=current_user.id,
                    challenge_id=challenge.id,
                    completed=True,
                    completed_at=datetime.now(timezone.utc)
                )
                db.add(progress)
            else:
                progress.completed = True
                progress.completed_at = datetime.now(timezone.utc)

        db.commit()
        db.refresh(submission)

    except Exception as e:
        db.rollback()
        submission.status = "SYSTEM_ERROR"
        submission.stderr = str(e)
        db.commit()

    return format_submission_response(submission, db)

@router.get("/submissions", response_model=List[SubmissionResponse])
def get_submissions(
    challenge_slug: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Submission).filter(Submission.user_id == current_user.id)
    if challenge_slug:
        challenge = db.query(Challenge).filter(Challenge.slug == challenge_slug).first()
        if challenge:
            query = query.filter(Submission.challenge_id == challenge.id)
            
    submissions = query.order_by(Submission.created_at.desc()).all()
    return [format_submission_response(s, db) for s in submissions]

@router.get("/submissions/{submission_id}", response_model=SubmissionResponse)
def get_submission(
    submission_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    submission = db.query(Submission).filter(Submission.id == submission_id).first()
    if not submission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Submission not found"
        )
        
    if submission.user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to view this submission"
        )
        
    return format_submission_response(submission, db)
