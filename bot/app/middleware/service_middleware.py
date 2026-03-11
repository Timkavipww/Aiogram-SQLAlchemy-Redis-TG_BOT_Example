from aiogram import BaseMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.user_service import UserService
from app.services.cache_service import CacheService


class ServiceMiddleware(BaseMiddleware):
    """Injector для сервисов (UserService, CacheService)"""

    async def __call__(self, handler, event, data):
        session: AsyncSession = data["session"]
        cache = CacheService()
        
        data["user_service"] = UserService(session, cache)
        data["cache"] = cache

        return await handler(event, data)