from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from loader import _


def get_menu_markup(super_admin: bool = False) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text=_("📝 Lists")))
    if super_admin: builder.add(KeyboardButton(text=_("🗄 Users")))
    builder.add(KeyboardButton(text=_("⚙️ Settings")))
    builder.adjust(2)

    builder.row(KeyboardButton(text=_("❌ Cancel")))

    return builder.as_markup(resize_keyboard=True)


def get_settings_markup(super_admin: bool = False) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text=_("📝 Lists")))
    if super_admin: builder.add(KeyboardButton(text=_("🗄 Users")))
    builder.add(KeyboardButton(text=_("⚙️ Settings")))
    builder.adjust(2)

    builder.row(KeyboardButton(text=_("❌ Cancel")))

    return builder.as_markup(resize_keyboard=True)
