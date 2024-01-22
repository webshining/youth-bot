from aiogram.filters import Command
from aiogram.types import Message

from app.filters import AdminFilter
from app.routers import admin_router as router
from database.models import User
from loader import _


@router.message(Command('users'), AdminFilter(super=True))
async def _users(message: Message):
    text, markup = await _get_users_data()
    await message.answer(text, reply_markup=markup)


async def _get_users_data():
    users = await User.get_all()
    text = _("<b>Users:</b>")
    text += _get_users_text(users)
    return text, None


def _get_users_text(users: list[User]) -> str:
    text = "\n" + _('Users is empty🫡')
    if users:
        text = ''
        for user in users:
            text += f'\n{"--" * 15}'
            for key, value in user.dict().items():
                text += f'\n|{key}: <b>{value}</b>'
    return text
