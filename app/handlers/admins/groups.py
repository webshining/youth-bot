from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app.routers import admin_router as router
from app.states import GroupState
from database.models import Group, User
from loader import _
from ..users.groups import _get_groups_data


@router.callback_query(lambda call: call.data.startswith('groups_create'))
async def _groups_call_create(call: CallbackQuery, state: FSMContext):
    text, markup = _("Enter group name:"), None
    await state.set_state(GroupState.create_name)
    await call.message.edit_text(text, reply_markup=markup)


@router.message(GroupState.create_name, F.text)
async def _groups_create(message: Message, state: FSMContext, user: User):
    await Group.create(name=message.text)
    text, markup = await _get_groups_data(user)

    await message.answer(text, reply_markup=markup)
    await state.set_state(None)
