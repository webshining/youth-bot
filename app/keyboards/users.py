from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.models import User


def get_users_markup(data: str, users: list[User]) -> InlineKeyboardMarkup:
    buttons = [InlineKeyboardButton(text=i.name, callback_data=f'{data}_{i.id}') for i in users]

    builder = InlineKeyboardBuilder()
    builder.add(*buttons)
    builder.adjust(2)

    return builder.as_markup()
