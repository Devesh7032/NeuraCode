import uuid
from datetime import datetime, timezone
from sqlalchemy import String, DateTime, ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

class Execution(Base):
    __tablename__ = "executions"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    challenge_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("challenges.id", ondelete="CASCADE"), nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="QUEUED")  # QUEUED, RUNNING, COMPLETED, FAILED, TIMEOUT, MEMORY_LIMIT, CANCELLED
    language: Mapped[str] = mapped_column(String(50), default="python")
    code: Mapped[str] = mapped_column(Text, nullable=False)
    runtime_ms: Mapped[int] = mapped_column(Integer, nullable=True)
    memory_bytes: Mapped[int] = mapped_column(Integer, nullable=True)
    stdout: Mapped[str] = mapped_column(Text, nullable=True)
    stderr: Mapped[str] = mapped_column(Text, nullable=True)
    exit_code: Mapped[int] = mapped_column(Integer, nullable=True)
    error_type: Mapped[str] = mapped_column(String(100), nullable=True)
    test_results: Mapped[str] = mapped_column(Text, nullable=True)  # Stores serialized JSON list of test case results
    visualization: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    started_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    finished_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    user: Mapped["User"] = relationship()
    challenge: Mapped["Challenge"] = relationship()
