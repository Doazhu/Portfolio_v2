from sqlalchemy.ext.asyncio import AsyncSession
from db.models import Message
from schemas.messages import MessageCreate

class MessageRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, msg: MessageCreate) -> Message:
        db_message = Message(
            name=msg.name,
            email=msg.email,
            subject=msg.subject,
            message=msg.message
        )
        self.db.add(db_message)
        await self.db.commit()
        # await self.db.refresh(db_message) # Not strictly needed if we don't return generated fields immediately unless requested
        return db_message

