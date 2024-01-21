from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.models import List
from loader import _


def get_lists_markup(data: str, items: list[List] = []) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.add(*[InlineKeyboardButton(text=i.name, callback_data=f'{data}_{i.id}') for i in items])
    builder.adjust(2)

    builder.row(*[InlineKeyboardButton(text=_("➕ Create"), callback_data=f"{data}_create"),
                  InlineKeyboardButton(text=_("🔄 Refresh"), callback_data=f"{data}_refresh")])

    return builder.as_markup()
