from typing import List
from fastapi import APIRouter, Depends, HTTPException
from services.projects import ProjectService
from schemas.projects import ProjectOut, ProjectCreate, ProjectUpdate
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


@router.get("/slug/{slug}", response_model=ProjectOut)
async def get_project_by_slug(
    slug: str,
    service: ProjectService = Depends(get_project_service)
):
    project = await service.get_project_by_slug(slug)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.post("", response_model=ProjectOut, status_code=201)
async def create_project(
    data: ProjectCreate,
    service: ProjectService = Depends(get_project_service)
):
    return await service.create_project(data)


@router.put("/{project_id}", response_model=ProjectOut)
async def update_project(
    project_id: int,
    data: ProjectUpdate,
    service: ProjectService = Depends(get_project_service)
):
    return await service.update_project(project_id, data)


@router.delete("/{project_id}", status_code=204)
async def delete_project(
    project_id: int,
    service: ProjectService = Depends(get_project_service)
):
    await service.delete_project(project_id)
    return None

