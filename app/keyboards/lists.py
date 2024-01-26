from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.models import List, User
from loader import _


def get_lists_markup(items: list[List], user: User) -> InlineKeyboardMarkup:
    buttons = [InlineKeyboardButton(text=i.name, callback_data=f'lists_read_{i.id}') for i in items]

    builder = InlineKeyboardBuilder()
    builder.add(*buttons)
    builder.adjust(2)
    buttons = []
    if user.is_admin():
        buttons = [InlineKeyboardButton(text=_("➕ Create"), callback_data=f'lists_create')]
    buttons.append(InlineKeyboardButton(text=_("🔄 Refresh"), callback_data=f'lists_refresh'))
    builder.row(*buttons)

    return builder.as_markup()


def get_list_markup(item: List, user: User) -> InlineKeyboardMarkup:
    buttons = []
    rules = item.rules(user)
    if "delete" in rules and item.removable:
        buttons.append(InlineKeyboardButton(text=_("❌ Delete"), callback_data=f'list_delete_{item.id}'))
    if "edit" in rules:
        buttons.append(InlineKeyboardButton(text=_("✏️ Edit"), callback_data=f'list_edit_{item.id}'))
    buttons.append(InlineKeyboardButton(text=_("✍️ Send message"), callback_data=f'list_send_{item.id}'))

    builder = InlineKeyboardBuilder()
    builder.add(*buttons)
    builder.adjust(2)

    builder.row(InlineKeyboardButton(text=_("⬅️ Back"), callback_data=f'list_back'))

    return builder.as_markup()
