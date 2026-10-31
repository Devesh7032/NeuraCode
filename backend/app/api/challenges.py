import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.core.database import get_db
from app.api.auth import get_current_user
from app.models.user import User, UserBookmark
from app.models.challenge import Challenge, ChallengeTest, ChallengeHint
from app.models.progress import LearningPath, UserProgress
from app.models.submission import Submission, SubmissionResult
from app.schemas.challenge import (
    ChallengeListResponse, 
    ChallengeDetailResponse, 
    LearningPathResponse
)
from app.schemas.submission import SubmissionCreate, SubmissionResponse

router = APIRouter(tags=["challenges"])

@router.get("/challenges", response_model=List[ChallengeListResponse])
def get_challenges(
    search: Optional[str] = None,
    category: Optional[str] = None,
    subcategory: Optional[str] = None,
    difficulty: Optional[str] = None,
    tag: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Challenge).filter(Challenge.status == "active")
    
    if search:
        query = query.filter(
            or_(
                Challenge.title.icontains(search),
                Challenge.description.icontains(search),
                Challenge.tags.icontains(search)
            )
        )
    if category and category != "All":
        query = query.filter(Challenge.category == category)
    if subcategory and subcategory != "All":
        query = query.filter(Challenge.subcategory == subcategory)
    if difficulty and difficulty != "All":
        query = query.filter(Challenge.difficulty == difficulty)
    if tag:
        query = query.filter(Challenge.tags.icontains(tag))
        
    return query.all()

@router.get("/challenges/{slug}", response_model=ChallengeDetailResponse)
def get_challenge(slug: str, db: Session = Depends(get_db)):
    challenge = db.query(Challenge).filter(Challenge.slug == slug, Challenge.status == "active").first()
    if not challenge:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Challenge with slug '{slug}' not found."
        )
    public_tests = [t for t in challenge.tests if t.visibility == "PUBLIC" or t.is_public]
    return {
        "id": challenge.id,
        "title": challenge.title,
        "slug": challenge.slug,
        "description": challenge.description,
        "concept": challenge.concept,
        "difficulty": challenge.difficulty,
        "category": challenge.category,
        "subcategory": challenge.subcategory,
        "prerequisites": challenge.prerequisites,
        "tags": challenge.tags,
        "status": challenge.status,
        "starter_code": challenge.starter_code,
        "constraints": challenge.constraints,
        "visualization_type": challenge.visualization_type,
        "visualization_config": challenge.visualization_config,
        "tests": public_tests,
        "hints": challenge.hints
    }

@router.get("/learning-paths", response_model=List[LearningPathResponse])
def get_learning_paths(db: Session = Depends(get_db)):
    return db.query(LearningPath).all()



@router.get("/bookmarks", response_model=List[str])
def get_user_bookmarks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    bookmarks = db.query(UserBookmark).filter(UserBookmark.user_id == current_user.id).all()
    challenge_ids = [b.challenge_id for b in bookmarks]
    challenges = db.query(Challenge).filter(Challenge.id.in_(challenge_ids)).all() if challenge_ids else []
    return [c.slug for c in challenges]

@router.post("/challenges/{slug}/bookmark")
def toggle_challenge_bookmark(
    slug: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    challenge = db.query(Challenge).filter(Challenge.slug == slug, Challenge.status == "active").first()
    if not challenge:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Challenge not found"
        )
    
    existing = db.query(UserBookmark).filter(
        UserBookmark.user_id == current_user.id,
        UserBookmark.challenge_id == challenge.id
    ).first()

    if existing:
        db.delete(existing)
        db.commit()
        return {"bookmarked": False}
    else:
        new_bookmark = UserBookmark(
            user_id=current_user.id,
            challenge_id=challenge.id
        )
        db.add(new_bookmark)
        db.commit()
        return {"bookmarked": True}

@router.get("/challenges/{slug}/solution")
def get_challenge_solution(
    slug: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    challenge = db.query(Challenge).filter(Challenge.slug == slug, Challenge.status == "active").first()
    if not challenge:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Challenge not found"
        )
    return {"reference_solution": challenge.reference_solution}
