from app.middleware import *
from app.bot import bot, dp
from app.db.init_db import init_models
from app.handlers import router
from app.config import *
from app.db.base import async_session
from asyncio import run

async def main():

    await init_models()
    config.validate_config()
    
    dp.include_router(router=router)
    
    dp.update.middleware(DbSessionMiddleware(async_session))
    dp.update.middleware(ServiceMiddleware())
    dp.update.middleware(EnsureUserMiddleware())



    logger.info("[MAIN] Bot started!")
    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    try:
        run(main())
    except KeyboardInterrupt as ex:
        logger.warning(f"[MAIN] Выключен вручную\n{ex}")
    except Exception as ex:
        logger.critical(f"[MAIN] Unhandled exception\n{ex}")