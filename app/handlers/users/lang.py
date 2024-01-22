from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from app.keyboards import get_lang_markup
from app.routers import user_router as router
from database.models import User
from loader import _


@router.message(Command("lang"))
async def _lang(message: Message):
    await message.answer(_('Select language:'), reply_markup=get_lang_markup())


@router.callback_query(lambda call: call.data.startswith("lang"))
async def _lang_change(call: CallbackQuery, user):
    await User.update(user.id, lang=call.data[5:])
    await call.message.edit_text(_("Success", locale=call.data[5:]))
