from typing import Any, Dict, Callable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery
from app.services.user_service import UserService
from app.config import logger

class EnsureUserMiddleware(BaseMiddleware):

    async def __call__(
        self,
        handler: Callable,
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:

        user_service: UserService | None = data.get("user_service")

        if user_service is None:
            return await handler(event, data)

        user = None

        if isinstance(event, Message):
            user = event.from_user

        elif isinstance(event, CallbackQuery):
            user = event.from_user

        if user:
            await user_service.ensure_user(
                user_id=user.id,
                username=user.username
            )

        return await handler(event, data)