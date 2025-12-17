from typing import List, Optional
from fastapi import HTTPException
from repositories.projects import ProjectRepository
from schemas.projects import ProjectCreate, ProjectUpdate
from db.models import Project


class ProjectService:
    def __init__(self, repository: ProjectRepository):
        self.repository = repository

    async def get_projects(self, featured_only: bool = False) -> List[Project]:
        return await self.repository.get_all(featured_only)

    async def get_project(self, project_id: int) -> Optional[Project]:
        return await self.repository.get_by_id(project_id)

    async def get_project_by_slug(self, slug: str) -> Optional[Project]:
        return await self.repository.get_by_slug(slug)

    async def create_project(self, data: ProjectCreate) -> Project:
        if await self.repository.slug_exists(data.slug):
            raise HTTPException(status_code=400, detail=f"Проект с slug '{data.slug}' уже существует")
        return await self.repository.create(data)

    async def update_project(self, project_id: int, data: ProjectUpdate) -> Project:
        if data.slug and await self.repository.slug_exists(data.slug, exclude_id=project_id):
            raise HTTPException(status_code=400, detail=f"Проект с slug '{data.slug}' уже существует")
        project = await self.repository.update(project_id, data)
        if not project:
            raise HTTPException(status_code=404, detail="Проект не найден")
        return project

    async def delete_project(self, project_id: int) -> bool:
        if not await self.repository.delete(project_id):
            raise HTTPException(status_code=404, detail="Проект не найден")
        return True

