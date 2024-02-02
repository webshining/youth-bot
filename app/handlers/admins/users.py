import csv
import io

from aiogram import html
from aiogram.filters import Command
from aiogram.types import BufferedInputFile, Message

from app.routers import super_admin_router as router
from database.models import User
from loader import _


@router.message(Command('users'))
async def _users(message: Message):
    text, file = await _get_users_data()
    text = _("<b>Users:</b>") + text
    await message.answer(text)
    await message.answer_document(BufferedInputFile(file, 'users.csv'))


async def _get_users_data():
    file = io.StringIO()
    writer = csv.writer(file)
    writer.writerow(list(User.__annotations__.keys()))
    for user in await User.get_all():
        writer.writerow(list(user.dict().values()))
    file.seek(0)
    file = io.BytesIO(file.getvalue().encode())
    file.seek(0)
    return _get_users_text(await User.get_all()), file.getvalue()


def _get_users_text(users: list[User]) -> str:
    text = "\n" + _('Users is empty🫡')
    if users:
        text = ''
        for user in users:
            text += f'\n|name: <b>{html.quote(str(user.name))}</b>'
    return text
