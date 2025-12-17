import logging
from fastapi import APIRouter, Depends
from services.messages import MessageService
from schemas.messages import MessageCreate
from depends import get_message_service

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/contact", tags=["contact"])

@router.post("", status_code=201)
async def send_message(
    msg: MessageCreate,
    service: MessageService = Depends(get_message_service)
):
    await service.send_message(msg)
    logger.info(f"📩 New message from {msg.email}")
    return {"status": "ok", "message": "Сообщение отправлено"}

