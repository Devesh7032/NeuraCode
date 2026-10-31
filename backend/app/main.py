from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.auth import router as auth_router
from app.api.challenges import router as challenges_router
from app.api.executions import router as executions_router
from app.api.submissions import router as submissions_router
from app.api.tutor import router as tutor_router
from app.seed import seed_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Run DB creation and seed data automatically on startup
    try:
        seed_db()
    except Exception as e:
        print(f"Startup database seeding failed: {e}")
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

# Set CORS origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
def health_check():
    return {"status": "ok", "project": settings.PROJECT_NAME}

# Include routers
app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(challenges_router, prefix=settings.API_V1_STR)
app.include_router(executions_router, prefix=settings.API_V1_STR)
app.include_router(submissions_router, prefix=settings.API_V1_STR)
app.include_router(tutor_router, prefix=settings.API_V1_STR)
