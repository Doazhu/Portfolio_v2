from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from db.models import Settings as SettingsModel

class SettingsRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_key(self, key: str) -> Optional[SettingsModel]:
        result = await self.db.execute(select(SettingsModel).where(SettingsModel.key == key))
        return result.scalar_one_or_none()

