from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.models import List
from loader import _


def get_list_markup(data: str, item: List) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.add(*[InlineKeyboardButton(text=_("❌ Delete"), callback_data=f"{data}_delete_{item.id}"),
                  InlineKeyboardButton(text=_("✏️ Edit"), callback_data=f'{data}_edit_{item.id}')])

    return builder.as_markup()
