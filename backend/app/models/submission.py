import uuid
from datetime import datetime, timezone
from sqlalchemy import String, DateTime, ForeignKey, Integer, Text, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

class Submission(Base):
    __tablename__ = "submissions"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    challenge_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("challenges.id", ondelete="CASCADE"), nullable=False)
    code: Mapped[str] = mapped_column(Text, nullable=False)
    language: Mapped[str] = mapped_column(String(50), default="python")
    status: Mapped[str] = mapped_column(String(50), default="Pending") # Pending, Running, Passed, Failed, Error, Accepted, etc.
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Aggregated execution telemetry
    passed_tests: Mapped[int] = mapped_column(Integer, default=0)
    total_tests: Mapped[int] = mapped_column(Integer, default=0)
    score: Mapped[float] = mapped_column(Float, default=0.0)
    runtime_ms: Mapped[int] = mapped_column(Integer, nullable=True)
    memory_bytes: Mapped[int] = mapped_column(Integer, nullable=True)
    
    # Global output logs
    stdout: Mapped[str] = mapped_column(Text, nullable=True)
    stderr: Mapped[str] = mapped_column(Text, nullable=True)

    user: Mapped["User"] = relationship(back_populates="submissions")
    challenge: Mapped["Challenge"] = relationship(back_populates="submissions")
    
    # One-to-many relationship mapping individual test executions
    results: Mapped[list["SubmissionResult"]] = relationship(back_populates="submission", cascade="all, delete-orphan")

class SubmissionResult(Base):
    __tablename__ = "submission_results"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    submission_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("submissions.id", ondelete="CASCADE"), nullable=False)
    test_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("challenge_tests.id", ondelete="CASCADE"), nullable=True)
    
    status: Mapped[str] = mapped_column(String(50), nullable=False) # passed, failed, error
    runtime_ms: Mapped[int] = mapped_column(Integer, nullable=True)
    actual_output: Mapped[str] = mapped_column(Text, nullable=True)
    error_type: Mapped[str] = mapped_column(String(100), nullable=True)
    error_message: Mapped[str] = mapped_column(Text, nullable=True)

    submission: Mapped["Submission"] = relationship(back_populates="results")
