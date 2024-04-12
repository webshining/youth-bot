from aiogram import Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, ErrorEvent
from aiogram.fsm.context import FSMContext

from .admins import admin_router, super_admin_router
from .users import router as user_router
from app.filters import AdminFilter
from utils import logger


def setup_handlers(dp: Dispatcher) -> None:
    @dp.errors()
    async def _error(event: ErrorEvent):
        logger.error(event.exception)

    @dp.message(Command('cancel'))
    async def _cancel(message: Message, state: FSMContext):
        await message.delete()
        await state.set_state(None)

    super_admin_router.callback_query.filter(AdminFilter(super=True))
    super_admin_router.message.filter(AdminFilter(super=True))
    admin_router.callback_query.filter(AdminFilter())
    admin_router.message.filter(AdminFilter())
    dp.include_routers(user_router, admin_router, super_admin_router)
