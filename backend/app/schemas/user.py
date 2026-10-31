import uuid
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class UserLogin(UserBase):
    password: str

class ProfileBase(BaseModel):
    display_name: Optional[str] = None
    avatar_url: Optional[str] = None
    bio: Optional[str] = None

class ProfileResponse(ProfileBase):
    xp: int
    
    class Config:
        from_attributes = True

class UserStreakResponse(BaseModel):
    current_streak: int
    longest_streak: int
    last_active: Optional[datetime] = None

    class Config:
        from_attributes = True

class UserProgressResponse(BaseModel):
    challenge_id: uuid.UUID
    completed: bool

    class Config:
        from_attributes = True

class UserSubmissionSummary(BaseModel):
    challenge_id: uuid.UUID
    status: str

    class Config:
        from_attributes = True

class UserResponse(UserBase):
    id: uuid.UUID
    is_active: bool
    is_superuser: bool
    created_at: datetime
    profile: Optional[ProfileResponse] = None
    streak: Optional[UserStreakResponse] = None
    progress: List[UserProgressResponse] = []
    submissions: List[UserSubmissionSummary] = []

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[str] = None
