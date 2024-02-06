from aiogram.filters import Command
from aiogram.types import Message

from app.routers import admin_router as router
from database.models import Need
from loader import _


@router.message(Command("needs"))
async def _needs(message: Message):
    needs = await Need.get_all()
    text = "\n\n".join([i.text for i in needs]) if needs else _('No needs🫡')
    await message.answer(text)


@router.message(Command("needs_clear"))
async def _needs_clear(message: Message):
    for i in await Need.get_all():
        await Need.delete(i.id)
    await message.answer(_("Success"))
