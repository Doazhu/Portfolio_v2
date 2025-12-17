from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from db.models import Skill

class SkillRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self, category: Optional[str] = None) -> List[Skill]:
        query = select(Skill).order_by(Skill.order)
        if category:
            query = query.where(Skill.category == category)
        result = await self.db.execute(query)
        return result.scalars().all()

