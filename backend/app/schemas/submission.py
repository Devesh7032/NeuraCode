import uuid
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict

class SubmissionCreate(BaseModel):
    code: str
    language: str = "python"

class SubmissionResultResponse(BaseModel):
    id: uuid.UUID
    submission_id: uuid.UUID
    test_id: Optional[uuid.UUID] = None
    status: str
    runtime_ms: Optional[int] = None
    actual_output: Optional[str] = None
    error_type: Optional[str] = None
    error_message: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class SubmissionResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    challenge_id: uuid.UUID
    code: str
    language: str
    status: str
    created_at: datetime
    passed_tests: int
    total_tests: int
    score: float
    runtime_ms: Optional[int] = None
    memory_bytes: Optional[int] = None
    stdout: Optional[str] = None
    stderr: Optional[str] = None
    results: List[SubmissionResultResponse] = []

    model_config = ConfigDict(from_attributes=True)
