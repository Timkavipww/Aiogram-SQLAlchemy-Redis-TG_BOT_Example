from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

def get_phone_keyboard() -> ReplyKeyboardMarkup:
    """Клавиатура для запроса телефона"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Поделиться телефоном", style='primary', request_contact=True, icon_custom_emoji_id='5276238731815165770')],
            [KeyboardButton(text="Отмена", style="danger", icon_custom_emoji_id='5787173538905460509')]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

def get_location_keyboard() -> ReplyKeyboardMarkup:
    """Клавиатура для запроса локации"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Поделиться локацией", style='primary', request_location=True, icon_custom_emoji_id='5350747347724810871')],
            [KeyboardButton(text="Отмена", style="danger", icon_custom_emoji_id='5787173538905460509')]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

def get_empty_keyboard() -> ReplyKeyboardMarkup:
    """Пустая клавиатура для скрытия кнопок"""
    return ReplyKeyboardRemove()