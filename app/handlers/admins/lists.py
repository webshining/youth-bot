from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app.routers import admin_router as router
from app.states import ListState
from database.models import List, User
from loader import _
from ..users.lists import _get_lists_data


@router.callback_query(lambda call: call.data.startswith('lists_create'))
async def _lists_call_create(call: CallbackQuery, state: FSMContext):
    text, markup = _("Enter list name:"), None
    await state.set_state(ListState.create_name)
    await call.message.edit_text(text, reply_markup=markup)


@router.message(ListState.create_name)
async def _lists_create(message: Message, state: FSMContext, user: User):
    await List.create(name=message.text)
    text, markup = await _get_lists_data(user.is_admin())

    await message.answer(text, reply_markup=markup)
    await state.set_state(None)
