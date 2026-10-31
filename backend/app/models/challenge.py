import uuid
from datetime import datetime, timezone
from sqlalchemy import String, DateTime, ForeignKey, Integer, Text, Boolean, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

class Challenge(Base):
    __tablename__ = "challenges"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    concept: Mapped[str] = mapped_column(Text, nullable=True)
    difficulty: Mapped[str] = mapped_column(String(50), nullable=False) # Easy, Medium, Hard
    category: Mapped[str] = mapped_column(String(100), nullable=False)
    subcategory: Mapped[str] = mapped_column(String(100), nullable=True)
    prerequisites: Mapped[str] = mapped_column(Text, nullable=True)
    tags: Mapped[str] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="active")
    starter_code: Mapped[str] = mapped_column(Text, nullable=False)
    reference_solution: Mapped[str] = mapped_column(Text, nullable=True)
    constraints: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Challenge contract parameters
    challenge_type: Mapped[str] = mapped_column(String(50), default="FUNCTION") # FUNCTION, SCRIPT
    function_name: Mapped[str] = mapped_column(String(100), nullable=True)
    function_signature: Mapped[str] = mapped_column(String(255), nullable=True)
    input_schema: Mapped[str] = mapped_column(Text, nullable=True) # JSON string schema
    output_schema: Mapped[str] = mapped_column(Text, nullable=True) # JSON string schema
    evaluation_type: Mapped[str] = mapped_column(String(50), nullable=True) # Default evaluation type
    visualization_type: Mapped[str] = mapped_column(String(50), nullable=True)
    visualization_config: Mapped[str] = mapped_column(Text, nullable=True)

    tests: Mapped[list["ChallengeTest"]] = relationship(back_populates="challenge", cascade="all, delete-orphan")
    hints: Mapped[list["ChallengeHint"]] = relationship(back_populates="challenge", cascade="all, delete-orphan")
    submissions: Mapped[list["Submission"]] = relationship(back_populates="challenge", cascade="all, delete-orphan")
    progress_items: Mapped[list["UserProgress"]] = relationship(back_populates="challenge", cascade="all, delete-orphan")
    learning_path_items: Mapped[list["LearningPathItem"]] = relationship(back_populates="challenge", cascade="all, delete-orphan")
    tutor_conversations: Mapped[list["TutorConversation"]] = relationship(back_populates="challenge", cascade="all, delete-orphan")

class ChallengeTest(Base):
    __tablename__ = "challenge_tests"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    challenge_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("challenges.id", ondelete="CASCADE"), nullable=False)
    input_data: Mapped[str] = mapped_column(Text, nullable=False)
    expected_output: Mapped[str] = mapped_column(Text, nullable=False)
    is_public: Mapped[bool] = mapped_column(Boolean, default=True) # Backwards compat

    # Upgraded test parameters
    name: Mapped[str] = mapped_column(String(255), nullable=True)
    visibility: Mapped[str] = mapped_column(String(50), default="PUBLIC") # PUBLIC, HIDDEN
    evaluation_type: Mapped[str] = mapped_column(String(50), default="EXACT") # EXACT, FLOAT_TOLERANCE, ARRAY_TOLERANCE, etc.
    tolerance: Mapped[float] = mapped_column(Float, default=1e-4, nullable=True)
    metric: Mapped[str] = mapped_column(String(100), nullable=True)
    threshold: Mapped[float] = mapped_column(Float, nullable=True)
    weight: Mapped[float] = mapped_column(Float, default=1.0, nullable=True)
    order: Mapped[int] = mapped_column(Integer, default=0, nullable=True)
    enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    challenge: Mapped["Challenge"] = relationship(back_populates="tests")

class ChallengeHint(Base):
    __tablename__ = "challenge_hints"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    challenge_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("challenges.id", ondelete="CASCADE"), nullable=False)
    hint_text: Mapped[str] = mapped_column(Text, nullable=False)
    order_index: Mapped[int] = mapped_column(Integer, default=0)

    challenge: Mapped["Challenge"] = relationship(back_populates="hints")
