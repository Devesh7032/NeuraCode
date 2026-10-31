import re
import json
from typing import Dict, Any, Optional, List
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.challenge import Challenge, ChallengeTest
from app.models.submission import Submission
from app.models.progress import UserProgress, LearningPath, LearningPathItem
from app.models.execution import Execution

class TutorContextBuilder:
    @staticmethod
    def sanitize_input(text: str) -> str:
        """Sanitizes user input to prevent prompt injection and system override attempts."""
        if not text:
            return ""
        # Remove common prompt injection phrases
        patterns = [
            r"(?i)ignore\s+(all\s+)?(previous|prior)\s+instructions?",
            r"(?i)system\s+prompt",
            r"(?i)reveal\s+(the\s+)?(reference\s+solution|hidden\s+tests)",
            r"(?i)act\s+as\s+a\s+DAN",
            r"(?i)you\s+are\s+now\s+free"
        ]
        sanitized = text
        for p in patterns:
            sanitized = re.sub(p, "[filtered_phrase]", sanitized)
        return sanitized

    @classmethod
    def build_context(
        cls,
        db: Session,
        user: User,
        challenge: Challenge,
        code: Optional[str] = None,
        action_type: str = "CHAT",
        hint_level: Optional[int] = 1,
        custom_inputs: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Builds a comprehensive, sanitized learning context for the AI Tutor.
        Explicitly excludes reference_solution, hidden tests, and secrets.
        """
        # 1. Challenge Metadata
        challenge_info = {
            "title": challenge.title,
            "slug": challenge.slug,
            "category": challenge.category,
            "subcategory": challenge.subcategory,
            "difficulty": challenge.difficulty,
            "description": challenge.description,
            "concept": challenge.concept or "",
            "constraints": challenge.constraints or "",
            "prerequisites": challenge.prerequisites or "",
            "tags": challenge.tags or "",
            "visualization_type": challenge.visualization_type or "None"
        }

        # 2. Public Test Cases ONLY (Filter out all hidden test inputs and expected outputs)
        public_tests = [
            {
                "input_data": t.input_data,
                "expected_output": t.expected_output
            }
            for t in challenge.tests if t.visibility == "PUBLIC" or t.is_public
        ]

        # 3. User Progress & Learning Path
        user_progress_records = db.query(UserProgress).filter(UserProgress.user_id == user.id, UserProgress.completed == True).all()
        completed_challenge_ids = {p.challenge_id for p in user_progress_records}
        completed_challenges = db.query(Challenge.slug).filter(Challenge.id.in_(completed_challenge_ids)).all() if completed_challenge_ids else []
        completed_slugs = [c.slug for c in completed_challenges]

        # Check prerequisite completion status
        prereq_slugs = [p.strip() for p in (challenge.prerequisites or "").split(",") if p.strip()]
        missing_prereqs = [p for p in prereq_slugs if p not in completed_slugs]

        # 4. Submission & Execution History (Public diagnostics only)
        latest_sub = db.query(Submission).filter(
            Submission.user_id == user.id,
            Submission.challenge_id == challenge.id
        ).order_by(Submission.created_at.desc()).first()

        latest_exec = db.query(Execution).filter(
            Execution.user_id == user.id,
            Execution.challenge_id == challenge.id
        ).order_by(Execution.started_at.desc()).first()

        submission_info = None
        if latest_sub:
            # Mask results for hidden test cases
            safe_results = []
            test_visibility = {t.id: t.visibility for t in challenge.tests}
            for r in latest_sub.results:
                vis = test_visibility.get(r.test_id, "PUBLIC")
                if vis != "HIDDEN":
                    safe_results.append({
                        "status": r.status,
                        "actual_output": r.actual_output,
                        "error_message": r.error_message
                    })
                else:
                    safe_results.append({
                        "status": r.status,
                        "actual_output": "[Hidden Test]",
                        "error_message": "[Hidden Test Case Outcome]"
                    })
                    
            submission_info = {
                "status": latest_sub.status,
                "passed_tests": latest_sub.passed_tests,
                "total_tests": latest_sub.total_tests,
                "code": cls.sanitize_input(latest_sub.code),
                "stdout": cls.sanitize_input(latest_sub.stdout or ""),
                "stderr": cls.sanitize_input(latest_sub.stderr or ""),
                "results": safe_results
            }

        # 5. Visualization Trace Data (if available)
        visualization_info = None
        if latest_exec and latest_exec.visualization:
            try:
                visualization_info = json.loads(latest_exec.visualization)
            except Exception:
                visualization_info = None

        # 6. Next Recommended Challenge
        next_challenge = None
        lp_item = db.query(LearningPathItem).filter(LearningPathItem.challenge_id == challenge.id).first()
        if lp_item:
            next_item = db.query(LearningPathItem).filter(
                LearningPathItem.learning_path_id == lp_item.learning_path_id,
                LearningPathItem.order_index > lp_item.order_index
            ).order_by(LearningPathItem.order_index.asc()).first()
            if next_item and next_item.challenge:
                next_challenge = {
                    "slug": next_item.challenge.slug,
                    "title": next_item.challenge.title
                }

        # Assembly
        return {
            "challenge": challenge_info,
            "public_tests": public_tests,
            "user_code": cls.sanitize_input(code or (latest_sub.code if latest_sub else challenge.starter_code)),
            "completed_challenges": completed_slugs,
            "missing_prerequisites": missing_prereqs,
            "latest_submission": submission_info,
            "visualization": visualization_info,
            "next_challenge": next_challenge,
            "action_type": action_type,
            "hint_level": hint_level or 1,
            "custom_inputs": custom_inputs or {}
        }
