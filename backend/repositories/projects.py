from typing import List, Optional
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from db.models import Project
from schemas.projects import ProjectCreate, ProjectUpdate


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

    async def get_by_slug(self, slug: str) -> Optional[Project]:
        result = await self.db.execute(select(Project).where(Project.slug == slug))
        return result.scalar_one_or_none()

    async def slug_exists(self, slug: str, exclude_id: Optional[int] = None) -> bool:
        query = select(Project.id).where(Project.slug == slug)
        if exclude_id:
            query = query.where(Project.id != exclude_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none() is not None

    async def create(self, data: ProjectCreate) -> Project:
        project = Project(**data.model_dump())
        self.db.add(project)
        await self.db.commit()
        await self.db.refresh(project)
        return project

    async def update(self, project_id: int, data: ProjectUpdate) -> Optional[Project]:
        project = await self.get_by_id(project_id)
        if not project:
            return None
        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(project, field, value)
        await self.db.commit()
        await self.db.refresh(project)
        return project

    async def delete(self, project_id: int) -> bool:
        project = await self.get_by_id(project_id)
        if not project:
            return False
        await self.db.delete(project)
        await self.db.commit()
        return True

