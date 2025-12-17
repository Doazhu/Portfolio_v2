from fastapi import APIRouter, Depends, HTTPException
from services.settings import SettingsService
from depends import get_settings_service

router = APIRouter(prefix="/api/settings", tags=["settings"])

@router.get("/{key}")
async def get_setting(
    key: str,
    service: SettingsService = Depends(get_settings_service)
):
    setting = await service.get_setting(key)
    if not setting:
        raise HTTPException(status_code=404, detail="Setting not found")
    return {"key": setting.key, "value": setting.value}

