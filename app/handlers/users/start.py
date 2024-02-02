from aiogram import html
from aiogram.filters import Command
from aiogram.types import Message

from app.commands import get_super_admins_commands, get_admins_commands, get_default_commands, \
    set_super_admins_commands, set_admins_commands, remove_user_commands
from app.routers import user_router as router
from database.models import User
from loader import _


@router.message(Command("start"))
async def _start(message: Message, user: User):
    if user.status == "super_admin":
        commands = get_super_admins_commands(user.lang)
    elif user.status == "admin":
        commands = get_admins_commands(user.lang)
    else:
        commands = get_default_commands(user.lang)

    text = _('Hello <b>{name}</b>') + "\n\nCommands:"
    for i in commands:
        text += f"\n{i.command} - {i.description.capitalize()}"
    await message.answer(text.format(name=html.quote(message.from_user.full_name)))

    try:
        if user.status == "super_admin":
            await set_super_admins_commands(user.id)
        elif user.status == "admin":
            await set_admins_commands(user.id)
        else:
            await remove_user_commands(user.id)
    except:
        pass
