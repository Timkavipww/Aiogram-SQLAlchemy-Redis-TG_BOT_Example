from typing import Any, Dict, Callable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery, Update
from app.services.user_service import UserService
from app.config import logger

class EnsureUserMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Update, data):
        if event.message:
            session = data.get("session")
            cache = data.get("cache")

            if session is None:
                logger.warning("[EnsureUserMiddleware] Нет session в данных")
                return await handler(event, data)

            service: UserService = UserService(session, cache=cache)
            user_id = event.message.from_user.id
            username = event.message.from_user.username
            user = await service.get_user(user_id)
            if not user:
                await service.create_user(user_id=user_id, username=username)
                logger.info(f"[EnsureUserMiddleware] Создан новый пользователь: {user_id}")

        return await handler(event, data)