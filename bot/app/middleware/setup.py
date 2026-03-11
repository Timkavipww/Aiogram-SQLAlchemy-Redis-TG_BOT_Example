from aiogram import Dispatcher

from app.middleware.error_middleware import ErrorMiddleware
from app.middleware.db_session_middleware import DbSessionMiddleware
from app.middleware.service_middleware import ServiceMiddleware
from app.middleware.ensure_user_middleware import EnsureUserMiddleware
from app.middleware.cache_middleware import CacheMiddleware


from app.db.base import async_session

def register_middlewares(dp: Dispatcher):

    dp.update.middleware(ErrorMiddleware())
    dp.update.middleware(DbSessionMiddleware(async_session))
    dp.update.middleware(ServiceMiddleware())
    dp.update.middleware(EnsureUserMiddleware())
    dp.update.middleware(CacheMiddleware())