from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from app.config import logger
from app.handlers.states import UserDataForm
from app.utils import get_phone_keyboard, get_location_keyboard, get_empty_keyboard

router = Router()

@router.message(Command("form"))
async def start_form(message: Message, state: FSMContext):
    """Начинает FSM для запроса контактных данных"""
    await state.set_state(UserDataForm.waiting_for_phone)
    await message.answer(
        "Пожалуйста, поделитесь своим телефоном:",
        reply_markup=get_phone_keyboard()
    )

@router.message(UserDataForm.waiting_for_phone, F.contact)
async def process_phone(message: Message, state: FSMContext):
    """Обрабатывает полученный телефон и переходит к запросу локации"""
    phone = message.contact.phone_number
    user_id = message.contact.user_id
    
    await state.update_data(phone=phone, user_id=user_id)
    await state.set_state(UserDataForm.waiting_for_location)
    
    await message.answer(
        f"Спасибо! Телефон: {phone}\n\nТеперь поделитесь вашей локацией:",
        reply_markup=get_location_keyboard()
    )

@router.message(UserDataForm.waiting_for_location, F.location)
async def process_location(message: Message, state: FSMContext):
    """Обрабатывает полученную локацию и завершает FSM"""
    location = message.location
    data = await state.get_data()
    
    phone = data.get("phone")
    latitude = location.latitude
    longitude = location.longitude
    
    result_text = (
        f"✅ Спасибо за информацию!\n\n"
        f"📱 Телефон: {phone}\n"
        f"📍 Локация: {latitude}, {longitude}"
    )
    
    await message.answer(result_text, reply_markup=get_empty_keyboard())
    
    await state.clear()

# ============ Отмена ============

@router.message(UserDataForm.waiting_for_phone, F.text == "Отмена")
@router.message(UserDataForm.waiting_for_location, F.text == "Отмена")
async def cancel_form(message: Message, state: FSMContext):
    """Отмена заполнения формы"""
    await state.clear()
    await message.answer(
        "Заполнение формы отменено.",
        reply_markup=get_empty_keyboard()
    )

# ============ Валидация ============

@router.message(UserDataForm.waiting_for_phone)
async def invalid_phone_input(message: Message):
    """Обработка неправильного ввода на этапе запроса телефона"""
    await message.answer("❌ Пожалуйста, используйте кнопку '📱 Поделиться телефоном'")

@router.message(UserDataForm.waiting_for_location)
async def invalid_location_input(message: Message):
    """Обработка неправильного ввода на этапе запроса локации"""
    await message.answer("❌ Пожалуйста, используйте кнопку '📍 Поделиться локацией'")