from typing import List, Optional
from repositories.skills import SkillRepository
from db.models import Skill

class SkillService:
    def __init__(self, repository: SkillRepository):
        self.repository = repository

    async def get_skills(self, category: Optional[str] = None) -> List[Skill]:
        return await self.repository.get_all(category)

