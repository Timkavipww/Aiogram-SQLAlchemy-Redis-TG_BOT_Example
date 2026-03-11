from aiogram import BaseMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.user_service import UserService

class ServiceMiddleware(BaseMiddleware):

    async def __call__(self, handler, event, data):

        session: AsyncSession = data["session"]

        data["user_service"] = UserService(session)

        return await handler(event, data)