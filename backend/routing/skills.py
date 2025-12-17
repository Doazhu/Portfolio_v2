from typing import List
from fastapi import APIRouter, Depends
from services.skills import SkillService
from schemas.skills import SkillOut
from depends import get_skill_service

router = APIRouter(prefix="/api/skills", tags=["skills"])

@router.get("", response_model=List[SkillOut])
async def get_skills(
    category: str | None = None,
    service: SkillService = Depends(get_skill_service)
):
    return await service.get_skills(category)

