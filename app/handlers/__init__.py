from aiogram import Dispatcher
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import ErrorEvent, Message

from app.filters import AdminFilter
from utils import logger

from .admins import admin_router, super_admin_router
from .users import router as user_router


def setup_handlers(dp: Dispatcher) -> None:
    @dp.error()
    async def _error(event: ErrorEvent):
        logger.exception(event.exception)

    @dp.message(Command('cancel'))
    async def _cancel(message: Message, state: FSMContext):
        await message.delete()
        await state.set_state(None)

    super_admin_router.callback_query.filter(AdminFilter(super=True))
    super_admin_router.message.filter(AdminFilter(super=True))
    admin_router.callback_query.filter(AdminFilter())
    admin_router.message.filter(AdminFilter())
    dp.include_routers(user_router, admin_router, super_admin_router)
