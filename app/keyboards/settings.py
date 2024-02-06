from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from loader import i18n, _


def get_settings_markup(action: str = None, notifications: bool = True, lang: str = "en") -> InlineKeyboardMarkup:
    if action == "lang":
        buttons = [InlineKeyboardButton(text=i.upper(), callback_data=f'settings_lang_{i}') for i in
                   i18n.available_locales]
        buttons.append(InlineKeyboardButton(text=_("⬅️ Back", locale=lang), callback_data="settings_back"))
    else:
        buttons = [InlineKeyboardButton(text=_("🌎Language", locale=lang), callback_data="settings_lang"),
                   InlineKeyboardButton(
                       text=_("🔔Notifications: On", locale=lang) if notifications else _("🔕Notifications: Off",
                                                                                         locale=lang),
                       callback_data="settings_notifications")]

    builder = InlineKeyboardBuilder()
    builder.add(*buttons)
    builder.adjust(3)

    return builder.as_markup()
