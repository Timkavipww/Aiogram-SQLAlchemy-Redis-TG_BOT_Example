from aiogram import BaseMiddleware
from app.services.cache_service import CacheService
from typing import Dict, Any

class CacheMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data: Dict[str, Any]):
        data["cache"] = CacheService()
        return await handler(event, data)