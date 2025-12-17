from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db.session import get_db

from repositories.projects import ProjectRepository
from repositories.skills import SkillRepository
from repositories.messages import MessageRepository
from repositories.settings import SettingsRepository

from services.projects import ProjectService
from services.skills import SkillService
from services.messages import MessageService
from services.settings import SettingsService

# Projects
def get_project_repository(db: AsyncSession = Depends(get_db)) -> ProjectRepository:
    return ProjectRepository(db)

def get_project_service(repo: ProjectRepository = Depends(get_project_repository)) -> ProjectService:
    return ProjectService(repo)

# Skills
def get_skill_repository(db: AsyncSession = Depends(get_db)) -> SkillRepository:
    return SkillRepository(db)

def get_skill_service(repo: SkillRepository = Depends(get_skill_repository)) -> SkillService:
    return SkillService(repo)

# Messages
def get_message_repository(db: AsyncSession = Depends(get_db)) -> MessageRepository:
    return MessageRepository(db)

def get_message_service(repo: MessageRepository = Depends(get_message_repository)) -> MessageService:
    return MessageService(repo)

# Settings
def get_settings_repository(db: AsyncSession = Depends(get_db)) -> SettingsRepository:
    return SettingsRepository(db)

def get_settings_service(repo: SettingsRepository = Depends(get_settings_repository)) -> SettingsService:
    return SettingsService(repo)

