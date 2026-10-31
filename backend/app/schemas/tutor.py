import uuid
from datetime import datetime
from typing import Optional, List, Any, Dict
from pydantic import BaseModel, Field

class TutorMessageResponse(BaseModel):
    id: uuid.UUID
    conversation_id: uuid.UUID
    role: str
    content: str
    action_type: str
    created_at: datetime

    class Config:
        from_attributes = True

class TutorConversationResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    challenge_id: uuid.UUID
    challenge_slug: str
    messages: List[TutorMessageResponse] = []
    created_at: datetime

    class Config:
        from_attributes = True

class TutorChatRequest(BaseModel):
    challenge_slug: str
    message: str = Field(..., max_length=2000)
    action_type: Optional[str] = "CHAT" # EXPLAIN_CONCEPT, EXPLAIN_CODE, GIVE_HINT, EXPLAIN_ERROR, EXPLAIN_GRAPH, NEXT_RECOMMENDATION, CHAT
    code: Optional[str] = None
    hint_level: Optional[int] = 1
    custom_inputs: Optional[Dict[str, Any]] = None

class TutorChatResponse(BaseModel):
    id: uuid.UUID
    conversation_id: uuid.UUID
    role: str
    content: str
    action_type: str
    suggested_actions: List[str] = []
    next_challenge_slug: Optional[str] = None
    next_challenge_title: Optional[str] = None
    created_at: datetime
