from typing import List
from fastapi import APIRouter, Depends, HTTPException
from services.projects import ProjectService
from schemas.projects import ProjectOut
from depends import get_project_service

router = APIRouter(prefix="/api/projects", tags=["projects"])

@router.get("", response_model=List[ProjectOut])
async def get_projects(
    featured_only: bool = False,
    service: ProjectService = Depends(get_project_service)
):
    return await service.get_projects(featured_only)

@router.get("/{project_id}", response_model=ProjectOut)
async def get_project(
    project_id: int,
    service: ProjectService = Depends(get_project_service)
):
    project = await service.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

