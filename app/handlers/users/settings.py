from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from app.keyboards import get_settings_markup
from app.routers import user_router as router
from database.models import User
from loader import _


@router.message(Command("settings"))
async def _settings(message: Message, user: User):
    await message.answer(_('⚙️Settings:'),
                         reply_markup=get_settings_markup(notifications=user.notifications, lang=user.lang))


@router.callback_query(lambda call: call.data.startswith("settings"))
async def _settings_call(call: CallbackQuery, user):
    if call.data[9:].startswith("lang_"):
        user = await User.update(user.id, lang=call.data[14:])
        text, markup = _("⚙️Settings:", locale=user.lang), get_settings_markup(notifications=user.notifications,
                                                                               lang=user.lang)
    elif call.data[9:].startswith("notifications"):
        user = await User.update(user.id, notifications=not user.notifications)
        text, markup = _("⚙️Settings:"), get_settings_markup(notifications=user.notifications, lang=user.lang)
    else:
        text, markup = _("⚙️Settings:"), get_settings_markup(action=call.data[9:], notifications=user.notifications,
                                                             lang=user.lang)
    try:
        await call.message.edit_text(text=text, reply_markup=markup)
    except:
        pass
