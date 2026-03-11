from aiogram import BaseMiddleware
from typing import Any, Dict, Callable
from aiogram.types import TelegramObject, Message
from app.config import logger, config
import traceback
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from app.bot import bot as tg_bot

MAX_TRACEBACK_LENGTH = 1000

class ErrorMiddleware(BaseMiddleware):

    async def __call__(self, handler: Callable, event: TelegramObject, data: Dict[str, Any]) -> Any:
        try:
            return await handler(event, data)
        except asyncio.CancelledError:
            raise
        except Exception as e:
            tb = traceback.format_exc()
            logger.exception(f"[ErrorMiddleware] Unhandled exception: {e}\n{tb}")

            session = data.get("session")
            if isinstance(session, AsyncSession):
                try:
                    await session.rollback()
                    logger.info("[ErrorMiddleware] Session rollback performed")
                except Exception:
                    logger.exception("[ErrorMiddleware] Failed to rollback session")

            try:
                if isinstance(event, Message) and event.from_user:
                    await tg_bot.send_message(
                        chat_id=event.from_user.id,
                        text="Произошла ошибка, администрация уведомлена."
                    )
            except Exception:
                logger.exception("[ErrorMiddleware] Failed to notify user about the error")

            try:
                tb_short = tb if len(tb) <= MAX_TRACEBACK_LENGTH else tb[-MAX_TRACEBACK_LENGTH:]
                admin_text = (
                    f"[Bot Error]\nException: {e}\n\nTraceback (last {MAX_TRACEBACK_LENGTH} chars):\n{tb_short}"
                )

                for admin_id in getattr(config, "ADMIN_IDS", []) or []:
                    try:
                        await tg_bot.send_message(chat_id=admin_id, text=admin_text)
                    except Exception:
                        logger.exception(f"[ErrorMiddleware] Failed to send error report to admin {admin_id}")

            except Exception:
                logger.exception("[ErrorMiddleware] Failed while sending admin notifications")

            raise