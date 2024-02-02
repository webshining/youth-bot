from aiogram import html
from aiogram.filters import Command
from aiogram.types import Message

from app.commands import set_admins_commands, set_super_admins_commands, remove_user_commands
from app.routers import user_router as router
from database.models import User
from loader import _


@router.message(Command("start"))
async def _start(message: Message, user: User):
    try:
        if user.status == "admin":
            await set_admins_commands(user.id)
        if user.status == "super_admin":
            await set_super_admins_commands(user.id)
        else:
            await remove_user_commands(user.id)
    except:
        pass

    await message.answer(_('Hello <b>{}</b>').format(html.quote(message.from_user.full_name)))
