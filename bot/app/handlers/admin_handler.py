from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()

@router.message(Command("admin"))
async def admin_cmd(message: Message):
    await message.answer("you are admin")