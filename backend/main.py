import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from core.config import settings
from db.session import engine
from db.models import Base, Project, Skill, Message, Settings
from core.admin import setup_admin

# Import routers
from routing.projects import router as projects_router
from routing.skills import router as skills_router
from routing.messages import router as messages_router
from routing.settings import router as settings_router

logging.basicConfig(
    level=logging.DEBUG if settings.DEBUG else logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Ensure tables are created (simplistic migration strategy)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("🚀 Application started")
    yield
    await engine.dispose()
    logger.info("👋 Application shutdown")


app = FastAPI(
    title="Doazhu Portfolio API",
    version="1.0.0",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
    lifespan=lifespan
)

app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

setup_admin(app, engine)

# Include routers
app.include_router(projects_router)
app.include_router(skills_router)
app.include_router(messages_router)
app.include_router(settings_router)

@app.get("/health")
async def health_check():
    return {"status": "ok", "version": "1.0.0"}
