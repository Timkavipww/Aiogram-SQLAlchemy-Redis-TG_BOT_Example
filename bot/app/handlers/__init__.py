from aiogram import Router

from app.handlers.start_handler import router as start_router
from app.handlers.admin_handler import router as admin_router

from app.middleware.admin_middleware import AdminMiddleware

router = Router()
admin_router.message.middleware(AdminMiddleware())

router.include_router(admin_router)
router.include_router(start_router)