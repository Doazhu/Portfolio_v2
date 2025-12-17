from pydantic import BaseModel
from typing import Optional

class SkillBase(BaseModel):
    name: str
    category: Optional[str] = None
    level: int = 50
    icon: Optional[str] = None
    order: int = 0

class SkillOut(SkillBase):
    id: int

    class Config:
        from_attributes = True

