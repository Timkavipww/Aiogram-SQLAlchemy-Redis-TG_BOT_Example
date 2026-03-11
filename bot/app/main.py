from app.middleware import register_middlewares
from app.db.init_db import init_models
from app.handlers import router
from app.config import logger
from app.bot import bot, dp
from asyncio import run

async def main():

    await init_models()
    
    dp.include_router(router=router)
    
    register_middlewares(dp)
    logger.info("[MAIN] Bot started!")
    await dp.start_polling(bot, skip_updates=False)

if __name__ == "__main__":
    try:
        run(main())
    except Exception as ex:
        logger.critical(f"[MAIN] Unhandled exception\n{ex}")