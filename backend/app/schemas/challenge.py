import uuid
from typing import Optional, List
from pydantic import BaseModel

class ChallengeTestResponse(BaseModel):
    id: uuid.UUID
    input_data: str
    expected_output: str
    is_public: bool

    class Config:
        from_attributes = True

class ChallengeHintResponse(BaseModel):
    id: uuid.UUID
    hint_text: str
    order_index: int

    class Config:
        from_attributes = True

class ChallengeListResponse(BaseModel):
    id: uuid.UUID
    title: str
    slug: str
    difficulty: str
    category: str
    subcategory: Optional[str] = None
    prerequisites: Optional[str] = None
    tags: Optional[str] = None
    status: str

    class Config:
        from_attributes = True

class ChallengeDetailResponse(BaseModel):
    id: uuid.UUID
    title: str
    slug: str
    description: str
    concept: Optional[str] = None
    difficulty: str
    category: str
    subcategory: Optional[str] = None
    prerequisites: Optional[str] = None
    tags: Optional[str] = None
    status: str
    starter_code: str
    constraints: Optional[str] = None
    visualization_type: Optional[str] = None
    visualization_config: Optional[str] = None
    tests: List[ChallengeTestResponse] = []
    hints: List[ChallengeHintResponse] = []

    class Config:
        from_attributes = True

class LearningPathItemResponse(BaseModel):
    id: uuid.UUID
    title: str
    order_index: int
    challenge: Optional[ChallengeListResponse] = None

    class Config:
        from_attributes = True

class LearningPathResponse(BaseModel):
    id: uuid.UUID
    title: str
    slug: str
    description: str
    category: str
    items: List[LearningPathItemResponse] = []

    class Config:
        from_attributes = True
