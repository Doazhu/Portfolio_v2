from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from db.models import Project
from schemas.projects import ProjectCreate

class ProjectRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self, featured_only: bool = False) -> List[Project]:
        query = select(Project).order_by(Project.order)
        if featured_only:
            query = query.where(Project.is_featured == True)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_by_id(self, project_id: int) -> Optional[Project]:
        result = await self.db.execute(select(Project).where(Project.id == project_id))
        return result.scalar_one_or_none()
    
    # Example Create (not in original main.py but good for completeness/validation example)
    async def create(self, project_data: ProjectCreate) -> Project:
        project = Project(**project_data.model_dump())
        self.db.add(project)
        await self.db.commit()
        await self.db.refresh(project)
        return project

