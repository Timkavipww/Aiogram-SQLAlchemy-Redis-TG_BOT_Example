from aiogram import Router
from aiogram.types import Message
from app.services.user_service import UserService
from app.services.cache_service import CacheService
from app.db.models.user import User

router = Router()


@router.message()
async def start_handler(
    message: Message,
    user_service: UserService,
    cache: CacheService
):
    
    cached_user = await cache.get(f"user:{message.from_user.id}")
    if cached_user:
        user = User(**cached_user)
    else:
        user = await user_service.get_or_create_user(
            user_id=message.from_user.id,
            username=message.from_user.username
        )
        await cache.set(f"user:{message.from_user.id}", user, expire=3600)
        
    await message.answer(f"Привет {user.username or 'друг'}")