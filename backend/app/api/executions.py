import uuid
import re
import json
from datetime import datetime, timezone
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.auth import get_current_user
from app.models.user import User
from app.models.challenge import Challenge, ChallengeTest
from app.models.execution import Execution
from app.schemas.execution import ExecutionRequest, ExecutionResponse
from app.execution.executor import run_in_sandbox
from app.core.config import settings

router = APIRouter(tags=["executions"])

def extract_function_name(starter_code: str, default_name: str) -> str:
    """Extracts the first defined python function name from starter code."""
    match = re.search(r"def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(", starter_code)
    if match:
        return match.group(1)
    return default_name

@router.post("/executions", response_model=ExecutionResponse)
def execute_code(
    req: ExecutionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Validate challenge slug exists and is active
    challenge = db.query(Challenge).filter(
        Challenge.slug == req.challenge_slug,
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

    # Validate rate limiting (maximum 2 concurrent executions per user)
    running_runs = db.query(Execution).filter(
        Execution.user_id == current_user.id,
        Execution.status.in_(["QUEUED", "RUNNING"])
    ).count()
    if running_runs >= 2:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many executions. Please wait before running another job."
        )

    # Initialize execution record
    execution = Execution(
        user_id=current_user.id,
        challenge_id=challenge.id,
        status="RUNNING",
        language=req.language,
        code=req.code,
        started_at=datetime.now(timezone.utc)
    )
    db.add(execution)
    db.commit()
    db.refresh(execution)

    from sqlalchemy import or_
    # Fetch public test cases
    public_tests = db.query(ChallengeTest).filter(
        ChallengeTest.challenge_id == challenge.id,
        or_(ChallengeTest.visibility == "PUBLIC", ChallengeTest.is_public == True)
    ).all()

    try:
        # Extract target function name
        func_name = extract_function_name(challenge.starter_code, challenge.slug.replace("-", "_"))
        
        # Format test cases list
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
            for t in public_tests
        ]

        # Run inside sandbox
        result = run_in_sandbox(
            code=req.code,
            language=req.language,
            function_name=func_name,
            test_cases=test_cases_list,
            challenge_slug=challenge.slug,
            custom_inputs=req.custom_inputs
        )

        # Update execution results
        execution.status = result["status"]
        execution.runtime_ms = result.get("runtime_ms")
        execution.stdout = result.get("stdout")
        execution.stderr = result.get("stderr")
        execution.exit_code = result.get("exit_code")
        execution.error_type = result.get("error_type")
        execution.test_results = json.dumps(result.get("tests", []))
        
        # Capture trace data if returned from the execution runner
        visualization_data = result.get("visualization")
        execution.visualization = json.dumps(visualization_data) if visualization_data else None
        
    except Exception as e:
        execution.status = "FAILED"
        execution.error_type = type(e).__name__
        execution.stderr = str(e)
        execution.test_results = json.dumps([])
        execution.visualization = None
        
    finally:
        execution.finished_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(execution)

    tests = json.loads(execution.test_results) if execution.test_results else []
    visualization = json.loads(execution.visualization) if execution.visualization else None
    return ExecutionResponse(
        id=execution.id,
        status=execution.status,
        language=execution.language,
        runtime_ms=execution.runtime_ms,
        memory_bytes=execution.memory_bytes,
        stdout=execution.stdout,
        stderr=execution.stderr,
        exit_code=execution.exit_code,
        error_type=execution.error_type,
        tests=tests,
        visualization=visualization,
        created_at=execution.created_at
    )

@router.get("/executions/{execution_id}", response_model=ExecutionResponse)
def get_execution_status(
    execution_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    execution = db.query(Execution).filter(
        Execution.id == execution_id,
        Execution.user_id == current_user.id
    ).first()
    if not execution:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Execution job not found or unauthorized."
        )

    tests = json.loads(execution.test_results) if execution.test_results else []
    visualization = json.loads(execution.visualization) if execution.visualization else None
    return ExecutionResponse(
        id=execution.id,
        status=execution.status,
        language=execution.language,
        runtime_ms=execution.runtime_ms,
        memory_bytes=execution.memory_bytes,
        stdout=execution.stdout,
        stderr=execution.stderr,
        exit_code=execution.exit_code,
        error_type=execution.error_type,
        tests=tests,
        visualization=visualization,
        created_at=execution.created_at
    )
