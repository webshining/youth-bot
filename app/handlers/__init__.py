from aiogram import Dispatcher

import app.handlers.cancel
# import app.handlers.error
from .admins import router as admin_router
from .users import router as user_router
from ..filters import AdminFilter


def setup_handlers(dp: Dispatcher) -> None:
    admin_router.callback_query.filter(AdminFilter())
    admin_router.message.filter(AdminFilter())
    dp.include_routers(user_router, admin_router)
