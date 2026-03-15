from aiogram import Router

from app.handlers.start_handler import router as start_router
from app.handlers.admin_handler import router as admin_router
from app.handlers.fsm_handler import router as fsm_router
from app.handlers.poll_handler import router as poll_router
from app.middleware.admin_middleware import AdminMiddleware

router = Router()
admin_router.message.middleware(AdminMiddleware())

router.include_router(admin_router)
router.include_router(fsm_router)
router.include_router(start_router)
router.include_router(poll_router)