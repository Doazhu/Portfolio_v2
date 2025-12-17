from typing import List, Optional
from repositories.projects import ProjectRepository
from schemas.projects import ProjectOut
from db.models import Project

class ProjectService:
    def __init__(self, repository: ProjectRepository):
        self.repository = repository

    async def get_projects(self, featured_only: bool = False) -> List[Project]:
        return await self.repository.get_all(featured_only)

    async def get_project(self, project_id: int) -> Optional[Project]:
        return await self.repository.get_by_id(project_id)

