from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from loader import i18n


def get_lang_markup() -> InlineKeyboardMarkup:
    buttons = [InlineKeyboardButton(text=i.upper(), callback_data=f'lang_{i}') for i in i18n.available_locales]

    builder = InlineKeyboardBuilder()
    builder.add(*buttons)
    
    return builder.as_markup()
