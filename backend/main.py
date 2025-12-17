import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel, EmailStr
from typing import List

from config import settings
from database import engine, async_session, Base, get_db
from models import Project, Skill, Message, Settings as SettingsModel
from admin import setup_admin

logging.basicConfig(
    level=logging.DEBUG if settings.DEBUG else logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
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


class ProjectOut(BaseModel):
    id: int
    title: str
    description: str | None
    image_url: str | None
    github_url: str | None
    live_url: str | None
    tech_stack: str | None
    is_featured: bool

    class Config:
        from_attributes = True


class SkillOut(BaseModel):
    id: int
    name: str
    category: str | None
    level: int
    icon: str | None

    class Config:
        from_attributes = True


class MessageCreate(BaseModel):
    name: str
    email: EmailStr
    subject: str | None = None
    message: str


@app.get("/health")
async def health_check():
    return {"status": "ok", "version": "1.0.0"}


@app.get("/api/projects", response_model=List[ProjectOut])
async def get_projects(featured_only: bool = False, db: AsyncSession = Depends(get_db)):
    query = select(Project).order_by(Project.order)
    if featured_only:
        query = query.where(Project.is_featured == True)
    result = await db.execute(query)
    return result.scalars().all()


@app.get("/api/projects/{project_id}", response_model=ProjectOut)
async def get_project(project_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Project).where(Project.id == project_id))
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@app.get("/api/skills", response_model=List[SkillOut])
async def get_skills(category: str | None = None, db: AsyncSession = Depends(get_db)):
    query = select(Skill).order_by(Skill.order)
    if category:
        query = query.where(Skill.category == category)
    result = await db.execute(query)
    return result.scalars().all()


@app.post("/api/contact", status_code=201)
async def send_message(msg: MessageCreate, db: AsyncSession = Depends(get_db)):
    db_message = Message(
        name=msg.name,
        email=msg.email,
        subject=msg.subject,
        message=msg.message
    )
    db.add(db_message)
    await db.commit()
    logger.info(f"📩 New message from {msg.email}")
    return {"status": "ok", "message": "Сообщение отправлено"}


@app.get("/api/settings/{key}")
async def get_setting(key: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(SettingsModel).where(SettingsModel.key == key))
    setting = result.scalar_one_or_none()
    if not setting:
        raise HTTPException(status_code=404, detail="Setting not found")
    return {"key": setting.key, "value": setting.value}
