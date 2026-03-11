from aiogram import BaseMiddleware
from aiogram.types import Message
from app.config import config

class AdminMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Message, data):
        if event.from_user.id not in config.ADMIN_IDS:
            return
        return await handler(event, data)
    