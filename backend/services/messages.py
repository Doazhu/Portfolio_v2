from repositories.messages import MessageRepository
from schemas.messages import MessageCreate
from db.models import Message

class MessageService:
    def __init__(self, repository: MessageRepository):
        self.repository = repository

    async def send_message(self, msg: MessageCreate) -> Message:
        # Business logic can go here (e.g. email notification)
        return await self.repository.create(msg)

