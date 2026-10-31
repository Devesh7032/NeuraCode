import uuid
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

class ExecutionRequest(BaseModel):
    challenge_slug: str
    code: str
    language: str = "python"
    custom_inputs: Optional[dict] = None

class TestCaseResultSchema(BaseModel):
    id: str
    status: str  # passed, failed, error
    actual: Optional[str] = None
    expected: str
    error: Optional[str] = None

class ExecutionResponse(BaseModel):
    id: uuid.UUID
    status: str
    language: str
    runtime_ms: Optional[int] = None
    memory_bytes: Optional[int] = None
    stdout: Optional[str] = None
    stderr: Optional[str] = None
    exit_code: Optional[int] = None
    error_type: Optional[str] = None
    tests: List[TestCaseResultSchema] = []
    visualization: Optional[dict] = None
    created_at: datetime

    class Config:
        from_attributes = True
