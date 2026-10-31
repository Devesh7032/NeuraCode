import pytest
from unittest.mock import patch
from sqlalchemy.orm import sessionmaker
from app.models.user import User, UserBookmark
from app.models.challenge import Challenge, ChallengeTest, ChallengeHint
from app.models.submission import Submission
from app.models.progress import LearningPath, LearningPathItem, UserProgress
from app.seed import seed_db
from app.core.security import get_password_hash, verify_password

@pytest.fixture
def patch_seed(db):
    # Bind seed_db to the test database
    test_session_maker = sessionmaker(bind=db.bind)
    with patch("app.seed.SessionLocal", test_session_maker):
        with patch("app.seed.engine", db.bind):
            yield

def test_password_security():
    # Verify passwords are never plaintext
    password = "secret_password"
    hashed = get_password_hash(password)
    assert hashed != password
    assert verify_password(password, hashed)
    assert not verify_password("wrong_password", hashed)

def test_persistence_flow(client, db, patch_seed):
    # TEST 1: Register and Login Success
    reg_data = {"email": "persist_test@example.com", "password": "password123"}
    res_reg = client.post("/api/auth/register", json=reg_data)
    assert res_reg.status_code == 200
    
    res_login = client.post("/api/auth/login", json=reg_data)
    assert res_login.status_code == 200
    assert "access_token" in res_login.json()

    # TEST 2: Restart application/database initialization (re-run create_all + seed)
    seed_db()
    
    # Login still works
    res_login = client.post("/api/auth/login", json=reg_data)
    assert res_login.status_code == 200

    # TEST 3: Seed challenges again -> Login still works
    seed_db()
    res_login = client.post("/api/auth/login", json=reg_data)
    assert res_login.status_code == 200

def test_seed_idempotency(db, patch_seed):
    # TEST 4 & 10: Run seed twice/multiple times -> check counts
    seed_db()
    
    # Get initial counts
    challenges_count = db.query(Challenge).count()
    
    assert challenges_count > 0
    
    # Add a user to ensure it survives
    user = User(email="seed_user@example.com", hashed_password=get_password_hash("pass"))
    db.add(user)
    db.commit()
    
    # Seed again and again
    seed_db()
    seed_db()
    
    # Verify counts and survival
    assert db.query(Challenge).count() == challenges_count
    assert db.query(User).filter_by(email="seed_user@example.com").first() is not None

def test_relations_survive_initialization(db, patch_seed):
    # Seed initially
    seed_db()
    
    # Create user
    user = User(email="relation_test@example.com", hashed_password=get_password_hash("pass"))
    db.add(user)
    db.flush()
    
    # Get a challenge
    challenge = db.query(Challenge).first()
    assert challenge is not None
    
    # TEST 5: Create Bookmark
    bookmark = UserBookmark(user_id=user.id, challenge_id=challenge.id)
    db.add(bookmark)
    
    # TEST 6: Create Submission
    submission = Submission(
        user_id=user.id,
        challenge_id=challenge.id,
        code="def test(): pass",
        status="Accepted",
        passed_tests=1,
        total_tests=1
    )
    db.add(submission)
    
    # TEST 7: Create Progress
    progress = UserProgress(
        user_id=user.id,
        challenge_id=challenge.id,
        completed=True
    )
    db.add(progress)
    db.commit()
    
    # Re-run initialization
    seed_db()
    
    # Assert relations survived
    db.expire_all()
    assert db.query(UserBookmark).filter_by(user_id=user.id, challenge_id=challenge.id).first() is not None
    assert db.query(Submission).filter_by(user_id=user.id, challenge_id=challenge.id).first() is not None
    assert db.query(UserProgress).filter_by(user_id=user.id, challenge_id=challenge.id).first() is not None
