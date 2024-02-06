from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.models import User, Group
from loader import _


def get_groups_markup(groups: list[Group], user: User) -> InlineKeyboardMarkup:
    buttons = [InlineKeyboardButton(text=i.name, callback_data=f'groups_read_{i.id}') for i in groups]

    builder = InlineKeyboardBuilder()
    builder.add(*buttons)
    builder.adjust(2)
    buttons = []
    if user.is_admin():
        buttons = [InlineKeyboardButton(text=_("➕ Create"), callback_data=f'groups_create')]
    buttons.append(InlineKeyboardButton(text=_("🔄 Refresh"), callback_data=f'groups_refresh'))
    builder.row(*buttons)

    return builder.as_markup()


def get_group_markup(group: Group, user: User) -> InlineKeyboardMarkup:
    buttons = []
    rules = group.rules(user)
    if "delete" in rules and group.removable:
        buttons.append(InlineKeyboardButton(text=_("❌ Delete"), callback_data=f'group_delete_{group.id}'))
    if "edit" in rules:
        buttons.append(InlineKeyboardButton(text=_("✏️ Edit"), callback_data=f'group_edit_{group.id}'))
    buttons.append(InlineKeyboardButton(text=_("✍️ Send message"), callback_data=f'group_send_{group.id}'))

    builder = InlineKeyboardBuilder()
    builder.add(*buttons)
    builder.adjust(2)

    builder.row(InlineKeyboardButton(text=_("⬅️ Back"), callback_data=f'group_back'))

    return builder.as_markup()
