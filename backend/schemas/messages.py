from pydantic import BaseModel, EmailStr
from typing import Optional

class MessageBase(BaseModel):
    name: str
    email: EmailStr
    subject: Optional[str] = None
    message: str

class MessageCreate(MessageBase):
    pass

class MessageOut(MessageBase):
    id: int
    is_read: bool

    class Config:
        from_attributes = True

