from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.models import List
from loader import _


def get_lists_markup(items: list[List], is_admin: bool = False) -> InlineKeyboardMarkup:
    buttons = [InlineKeyboardButton(text=i.name, callback_data=f'lists_read_{i.id}') for i in items]

    builder = InlineKeyboardBuilder()
    builder.add(*buttons)
    builder.adjust(2)
    buttons = []
    if is_admin:
        buttons = [InlineKeyboardButton(text=_("➕ Create"), callback_data=f'lists_create')]
    buttons.append(InlineKeyboardButton(text=_("🔄 Refresh"), callback_data=f'lists_refresh'))
    builder.row(*buttons)

    return builder.as_markup()


def get_list_markup(id: int, rules: list[str] = []) -> InlineKeyboardMarkup:
    buttons = []
    if "delete" in rules:
        buttons.append(InlineKeyboardButton(text=_("❌ Delete"), callback_data=f'list_delete_{id}'))
    if "edit" in rules:
        buttons.append(InlineKeyboardButton(text=_("✏️ Edit"), callback_data=f'list_edit_{id}'))

    builder = InlineKeyboardBuilder()
    if "send" in rules:
        builder.row(InlineKeyboardButton(text=_("✍️ Send message"), callback_data=f'list_send_{id}'))
    builder.row(*buttons)
    builder.row(InlineKeyboardButton(text=_("⬅️ Back"), callback_data=f'list_back'))

    return builder.as_markup()
