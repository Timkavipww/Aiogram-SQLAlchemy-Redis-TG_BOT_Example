from aiogram import Router, F
from aiogram.types import Message, WebAppData, ContentType, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from app.config import logger
from app.handlers.states import UserDataForm
from app.utils import get_phone_keyboard, get_location_keyboard, get_empty_keyboard, generate_excel_file

import json

router = Router()

WEBAPP_URL = "https://terrance-helpless-tyron.ngrok-free.dev/"

# Обработчик команды /data_reply, который отправляет пользователю клавиатуру с кнопкой для открытия WebApp
# получаем данные из WebApp и логируем их, а также отправляем пользователю подтверждение с полученными данными
# Важно: для получения данных из WebApp, бот должен быть запущен на сервере, который доступен по HTTPS, и URL WebApp должен быть указан в настройках бота в Telegram Bot API.
# В данном примере мы используем ngrok для создания временного публичного URL, который перенаправляет на локальный сервер, где запущен бот. Не забудьте заменить WEBAPP_URL на ваш реальный URL WebApp.
# Также убедитесь, что WebApp отправляет данные в правильном формате, который ожидает бот (обычно это JSON), и что бот правильно обрабатывает эти данные.
# после нажатия кнопки пропадает клавиатура, так как мы используем one_time_keyboard=True, и пользователь видит только сообщение с подтверждением и полученными данными.
@router.message(Command("data_reply"))
async def start_handler(message: Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text="🚀 Открыть приложение",
                    web_app=WebAppInfo(url=WEBAPP_URL)
                )
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

    await message.answer(
        "Открой WebApp 👇",
        reply_markup=keyboard
    )

@router.message(F.content_type == ContentType.WEB_APP_DATA)
async def data_handler(message: Message):
    data = json.loads(message.web_app_data.data)
    logger.info(f"[DataHandler] Получены данные: {json.dumps(data, indent=2, ensure_ascii=False)}")

    # Проверяем, что прислано
    if data.get("type") == "excel":
        # Генерируем и отправляем Excel
        file = await generate_excel_file(data.get("payload", {}), title="Отправка Excel")
        await message.answer_document(file)
        await message.answer("✅ Excel-файл успешно сформирован!", reply_markup=get_empty_keyboard())
    else:
        # Отправляем обычный JSON
        await message.answer(
            f"✅ Данные успешно получены!\n\n<pre>{json.dumps(data, indent=2, ensure_ascii=False)}</pre>",
            parse_mode="HTML",
            reply_markup=get_empty_keyboard()
        )