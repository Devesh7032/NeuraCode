import uuid
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, Optional, Tuple, List
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.core.config import settings
from app.models.user import User
from app.models.challenge import Challenge
from app.models.tutor import TutorConversation, TutorMessage
from app.schemas.tutor import TutorChatRequest, TutorChatResponse, TutorConversationResponse, TutorMessageResponse
from app.services.ai_tutor.context_builder import TutorContextBuilder
from app.services.ai_tutor.gemini_provider import GeminiProvider
from app.services.ai_tutor.fallback_provider import FallbackProvider

# Simple in-memory rate limiting tracker: user_id -> List[datetime]
RATE_LIMIT_STORE: Dict[uuid.UUID, List[datetime]] = {}

class AITutorService:
    @staticmethod
    def check_rate_limit(user_id: uuid.UUID) -> None:
        """Enforces a maximum rate limit of requests per time window."""
        now = datetime.now(timezone.utc)
        window = timedelta(minutes=5)
        max_requests = settings.TUTOR_RATE_LIMIT_PER_WINDOW or 15

        user_history = RATE_LIMIT_STORE.get(user_id, [])
        # Filter timestamps within current 5-minute window
        valid_history = [t for t in user_history if (now - t) <= window]
        
        if len(valid_history) >= max_requests:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"AI Tutor rate limit exceeded ({max_requests} requests / 5 min). Please wait before asking another question."
            )
            
        valid_history.append(now)
        RATE_LIMIT_STORE[user_id] = valid_history

    @staticmethod
    def get_or_create_conversation(db: Session, user: User, challenge: Challenge) -> TutorConversation:
        """Retrieves or creates a persistent tutor conversation thread."""
        conversation = db.query(TutorConversation).filter(
            TutorConversation.user_id == user.id,
            TutorConversation.challenge_id == challenge.id
        ).first()

        if not conversation:
            conversation = TutorConversation(
                user_id=user.id,
                challenge_id=challenge.id
            )
            db.add(conversation)
            db.commit()
            db.refresh(conversation)

        return conversation

    @classmethod
    async def process_chat_request(
        cls,
        db: Session,
        user: User,
        req: TutorChatRequest
    ) -> TutorChatResponse:
        """Processes an AI Tutor interaction, constructs context, calls provider, and persists conversation."""
        # 1. Validate rate limit
        cls.check_rate_limit(user.id)

        # 2. Retrieve challenge
        challenge = db.query(Challenge).filter(
            Challenge.slug == req.challenge_slug,
            Challenge.status == "active"
        ).first()
        if not challenge:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Challenge '{req.challenge_slug}' not found."
            )

        # 3. Retrieve or create conversation
        conversation = cls.get_or_create_conversation(db, user, challenge)

        # 4. Build sanitized context
        context = TutorContextBuilder.build_context(
            db=db,
            user=user,
            challenge=challenge,
            code=req.code,
            action_type=req.action_type or "CHAT",
            hint_level=req.hint_level or 1,
            custom_inputs=req.custom_inputs
        )

        # 5. Select provider
        provider = GeminiProvider() if settings.GEMINI_API_KEY else FallbackProvider()

        system_instruction = (
            "You are NeuraCode AI Tutor, an intelligent AI/ML coding instructor.\n"
            "You are pair-programming with a developer learning AI/ML concepts.\n"
            "Guidelines:\n"
            "1. Be encouraging, precise, and concise.\n"
            "2. Never reveal reference_solution or hidden test cases.\n"
            "3. Help the learner understand concepts and debug mistakes step-by-step rather than giving away full answers immediately.\n"
            "4. Use clear GitHub-style markdown formatting (headings, code blocks, bold text)."
        )

        user_prompt = TutorContextBuilder.sanitize_input(req.message)

        # 6. Generate tutor response
        try:
            tutor_reply = await provider.generate_response(system_instruction, user_prompt, context)
        except Exception:
            fallback = FallbackProvider()
            tutor_reply = await fallback.generate_response(system_instruction, user_prompt, context)

        # 7. Persist user message & tutor reply
        user_msg = TutorMessage(
            conversation_id=conversation.id,
            role="user",
            content=user_prompt if user_prompt else f"[{req.action_type}]",
            action_type=req.action_type or "CHAT"
        )
        db.add(user_msg)

        assistant_msg = TutorMessage(
            conversation_id=conversation.id,
            role="assistant",
            content=tutor_reply,
            action_type=req.action_type or "CHAT"
        )
        db.add(assistant_msg)
        db.commit()
        db.refresh(assistant_msg)

        # 8. Suggested actions & Next recommendation
        suggested_actions = ["Explain Concept", "Give Hint", "Explain Code", "Explain Error"]
        if challenge.visualization_type:
            suggested_actions.append("Explain Graph")

        next_ch = context.get("next_challenge")

        return TutorChatResponse(
            id=assistant_msg.id,
            conversation_id=conversation.id,
            role="assistant",
            content=assistant_msg.content,
            action_type=assistant_msg.action_type,
            suggested_actions=suggested_actions,
            next_challenge_slug=next_ch.get("slug") if next_ch else None,
            next_challenge_title=next_ch.get("title") if next_ch else None,
            created_at=assistant_msg.created_at
        )

    @classmethod
    def get_conversation_history(
        cls,
        db: Session,
        user: User,
        challenge_slug: str
    ) -> TutorConversationResponse:
        """Returns past messages in active tutor conversation thread."""
        challenge = db.query(Challenge).filter(Challenge.slug == challenge_slug).first()
        if not challenge:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Challenge not found."
            )

        conversation = db.query(TutorConversation).filter(
            TutorConversation.user_id == user.id,
            TutorConversation.challenge_id == challenge.id
        ).first()

        if not conversation:
            # Return empty response
            return TutorConversationResponse(
                id=uuid.uuid4(),
                user_id=user.id,
                challenge_id=challenge.id,
                challenge_slug=challenge.slug,
                messages=[],
                created_at=datetime.now(timezone.utc)
            )

        messages_res = [
            TutorMessageResponse(
                id=m.id,
                conversation_id=m.conversation_id,
                role=m.role,
                content=m.content,
                action_type=m.action_type,
                created_at=m.created_at
            )
            for m in conversation.messages
        ]

        return TutorConversationResponse(
            id=conversation.id,
            user_id=conversation.user_id,
            challenge_id=conversation.challenge_id,
            challenge_slug=challenge.slug,
            messages=messages_res,
            created_at=conversation.created_at
        )

    @classmethod
    def clear_conversation_history(
        cls,
        db: Session,
        user: User,
        challenge_slug: str
    ) -> Dict[str, Any]:
        """Clears conversation history for the challenge."""
        challenge = db.query(Challenge).filter(Challenge.slug == challenge_slug).first()
        if not challenge:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Challenge not found."
            )

        conversation = db.query(TutorConversation).filter(
            TutorConversation.user_id == user.id,
            TutorConversation.challenge_id == challenge.id
        ).first()

        if conversation:
            db.delete(conversation)
            db.commit()

        return {"status": "cleared", "challenge_slug": challenge_slug}
