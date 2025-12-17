from typing import Optional
from repositories.settings import SettingsRepository
from db.models import Settings as SettingsModel

class SettingsService:
    def __init__(self, repository: SettingsRepository):
        self.repository = repository

    async def get_setting(self, key: str) -> Optional[SettingsModel]:
        return await self.repository.get_by_key(key)

