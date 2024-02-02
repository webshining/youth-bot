import asyncio

from aiogram import F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from app.filters import AdminFilter
from app.routers import admin_router as router
from app.states import Notify
from database.models import User
from loader import _
from utils import logger


@router.message(Command('notify'), AdminFilter(super=True))
async def _notify(message: Message, state: FSMContext):
    await message.answer(_("Enter message text:"))
    await state.set_state(Notify.text)


@router.message(F.text, Notify.text, AdminFilter(super=True))
async def _notify_to(message: Message, user: User, state: FSMContext):
    users = [i for i in await User.get_all() if i.id != user.id]
    for u in users:
        try:
            await message.copy_to(chat_id=u.id, reply_markup=None)
        except:
            logger.error(f"message for {u.id}-{u.name} was not sent")
        await asyncio.sleep(0.5)
    await state.set_state(None)
