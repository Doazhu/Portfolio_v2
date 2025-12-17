from pydantic import BaseModel
from typing import Optional

class SettingsOut(BaseModel):
    key: str
    value: Optional[str]

    class Config:
        from_attributes = True

