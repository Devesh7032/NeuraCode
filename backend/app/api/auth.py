import uuid
from datetime import datetime, timezone, timedelta
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.config import settings
from app.core.security import verify_password, get_password_hash, create_access_token
from app.models.user import User, Profile, UserStreak
from app.schemas.user import UserCreate, UserLogin, UserResponse, Token

router = APIRouter(prefix="/auth", tags=["auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login-form", auto_error=False)

def get_token_from_header_or_cookie(request: Request, token: Optional[str] = Depends(oauth2_scheme)) -> str:
    # Check authorization header first
    if token:
        return token
    # Fallback to cookie
    cookie_token = request.cookies.get("access_token")
    if cookie_token:
        # Standard format in cookie might be "Bearer <token>" or just "<token>"
        if cookie_token.startswith("Bearer "):
            return cookie_token.split(" ")[1]
        return cookie_token
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authenticated",
        headers={"WWW-Authenticate": "Bearer"},
    )

def get_current_user(
    db: Session = Depends(get_db), 
    token: str = Depends(get_token_from_header_or_cookie)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            print("[AUTH DEBUG] Token validation failed: INVALID_TOKEN (sub claim missing)")
            raise credentials_exception
    except JWTError as jwt_err:
        print(f"[AUTH DEBUG] Token validation failed: INVALID_TOKEN: {jwt_err}")
        raise credentials_exception
        
    try:
        user = db.query(User).filter(User.id == uuid.UUID(user_id)).first()
        if user is None:
            print("[AUTH DEBUG] Token validation failed: USER_NOT_FOUND")
            raise credentials_exception
        return user
    except Exception as db_err:
        print(f"[AUTH DEBUG] Token validation failed: DATABASE_ERROR: {db_err}")
        raise credentials_exception

@router.post("/register", response_model=UserResponse)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    user = db.query(User).filter(User.email == user_in.email).first()
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email address already exists in the system.",
        )
    
    # Create new User
    db_user = User(
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password)
    )
    db.add(db_user)
    db.flush() # populate user.id

    # Create empty Profile
    db_profile = Profile(
        user_id=db_user.id,
        display_name=user_in.email.split("@")[0],
        avatar_url=f"https://api.dicebear.com/7.x/bottts/svg?seed={db_user.email}",
        bio="New member of NeuraCode community."
    )
    db.add(db_profile)

    # Initialize UserStreak
    db_streak = UserStreak(
        user_id=db_user.id,
        current_streak=0,
        longest_streak=0,
        last_active=None
    )
    db.add(db_streak)

    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/login", response_model=Token)
def login(user_in: UserLogin, response: Response, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.email == user_in.email).first()
        if not user:
            print("[AUTH DEBUG] Login failed: USER_NOT_FOUND")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect email or password"
            )
            
        if not verify_password(user_in.password, user.hashed_password):
            print("[AUTH DEBUG] Login failed: INVALID_PASSWORD")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect email or password"
            )
            
        if not user.is_active:
            print("[AUTH DEBUG] Login failed: USER_INACTIVE")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Inactive user"
            )
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        print(f"[AUTH DEBUG] Login failed: DATABASE_ERROR: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Incorrect email or password"
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        user.id, expires_delta=access_token_expires
    )

    # Optional: Update user's last active streak timestamp
    if user.streak:
        now = datetime.now(timezone.utc)
        if user.streak.last_active is None:
            user.streak.current_streak = 1
            user.streak.longest_streak = 1
        else:
            delta = now.date() - user.streak.last_active.date()
            if delta.days == 1:
                user.streak.current_streak += 1
                if user.streak.current_streak > user.streak.longest_streak:
                    user.streak.longest_streak = user.streak.current_streak
            elif delta.days > 1:
                user.streak.current_streak = 1
        user.streak.last_active = now
        db.commit()

    # Set httponly cookie for easier integration if desired, but we also return token
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        samesite="lax",
        secure=False # set True in production
    )

    return {"access_token": access_token, "token_type": "bearer"}

# Form login support for Swagger UI Swagger
from fastapi.security import OAuth2PasswordRequestForm
@router.post("/login-form")
def login_form(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        user.id, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/logout")
def logout(response: Response):
    response.delete_cookie(key="access_token")
    return {"message": "Successfully logged out"}

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user
