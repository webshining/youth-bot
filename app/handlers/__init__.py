from aiogram import Dispatcher

import app.handlers.cancel
import app.handlers.error
from .admins import admin_router, super_admin_router
from .users import router as user_router
from ..filters import AdminFilter


def setup_handlers(dp: Dispatcher) -> None:
    super_admin_router.callback_query.filter(AdminFilter(super=True))
    super_admin_router.message.filter(AdminFilter(super=True))
    admin_router.callback_query.filter(AdminFilter())
    admin_router.message.filter(AdminFilter())
    dp.include_routers(user_router, admin_router, super_admin_router)
