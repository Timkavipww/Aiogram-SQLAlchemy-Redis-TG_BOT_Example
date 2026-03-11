from aiogram import Router
from aiogram.types import Message
from app.services.user_service import UserService

router = Router()


@router.message()
async def start_handler(
    message: Message,
    user_service: UserService
):

    user = await user_service.get_or_create_user(
        user_id=message.from_user.id,
        username=message.from_user.username
    )

    await message.answer(f"Привет {user.username or 'друг'}")