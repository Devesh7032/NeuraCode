from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.auth import get_current_user
from app.models.user import User
from app.schemas.tutor import (
    TutorChatRequest,
    TutorChatResponse,
    TutorConversationResponse
)
from app.services.ai_tutor.service import AITutorService

router = APIRouter(tags=["tutor"])

@router.post("/tutor/chat", response_model=TutorChatResponse)
async def chat_with_tutor(
    req: TutorChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Sends a question or quick action request to AI Tutor.
    Retrieves context-aware response based on challenge, user code, error diagnostics, and traces.
    """
    return await AITutorService.process_chat_request(db, current_user, req)

@router.get("/tutor/conversations/{challenge_slug}", response_model=TutorConversationResponse)
def get_tutor_conversation(
    challenge_slug: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieves the persistent AI Tutor conversation history for the current user and challenge.
    """
    return AITutorService.get_conversation_history(db, current_user, challenge_slug)

@router.delete("/tutor/conversations/{challenge_slug}")
def clear_tutor_conversation(
    challenge_slug: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Resets/clears conversation history for the active challenge.
    """
    return AITutorService.clear_conversation_history(db, current_user, challenge_slug)
