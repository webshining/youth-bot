from aiogram import html
from aiogram.filters import Command
from aiogram.types import Message

from app.routers import user_router as router
from loader import _


@router.message(Command("start"))
async def _start(message: Message):
    await message.answer(_('Hello <b>{}</b>').format(html.quote(message.from_user.full_name)))
