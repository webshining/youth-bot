from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_apply_markup(data: str, *args) -> InlineKeyboardMarkup:
    args = [str(i) for i in args]
    buttons = [InlineKeyboardButton(text="🆗", callback_data=f'{data}_{"_".join(args)}')]

    builder = InlineKeyboardBuilder()
    builder.add(*buttons)
    return builder.as_markup()
