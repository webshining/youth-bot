from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from app.filters import StatusFilter
from app.handlers.admins.users import _get_users_text
from app.keyboards import get_lists_markup, get_list_markup
from app.routers import admin_router as router
from app.states import ListStates
from database.models import List, get_session
from loader import _


@router.message(Command("lists"), StatusFilter("admin"))
async def _lists(message: Message):
    text, markup = await _get_lists_data()
    await message.answer(text, reply_markup=markup)


@router.message(Command("create_list"), StatusFilter("admin"))
async def _create_list(message: Message, state: FSMContext):
    await message.answer(_("Enter list name:"))
    await state.set_state(ListStates.create_name)


@router.message(ListStates.create_name, StatusFilter("admin"))
async def _create_list_name(message: Message, state: FSMContext):
    async with get_session() as session:
        await List.create(session, name=message.text)
    text, markup = await _get_lists_data()
    await message.answer(_("Success"), reply_markup=markup)
    await state.set_state(None)


@router.callback_query(lambda call: call.data.startswith("lists"))
async def _lists_call(call: CallbackQuery, state: FSMContext):
    if call.data[6:] == "create":
        await call.message.edit_text(_("Enter list name:"), reply_markup=None)
        await state.set_state(ListStates.create_name)
    elif call.data[6:] == "refresh":
        try:
            text, markup = await _get_lists_data()
            await call.message.edit_text(text, reply_markup=markup)
        except:
            pass
    else:
        text, markup = await _get_list_data(call.data[6:])
        await call.message.edit_text(text, reply_markup=markup)
    await call.answer()


@router.callback_query(lambda call: call.data.startswith("list"))
async def _list_call(call: CallbackQuery):
    if call.data[5:].startswith("delete"):
        async with get_session() as session:
            await List.delete(session, call.data[12:])
        text, markup = await _get_lists_data()
        await call.message.edit_text(_("Success"), reply_markup=markup)
    await call.answer(call.data)


async def _get_lists_data():
    async with get_session() as session:
        lists = await List.get_all(session)
    text = _("Select list:")
    markup = get_lists_markup("lists", lists)
    return text, markup


async def _get_list_data(id: int):
    async with get_session() as session:
        list = await List.get(session, id)
        if not list:
            lists = await List.get_all(session)
            text = _("List not found 🤷‍♂️")
            markup = get_lists_markup("lists", lists)
        else:
            text = _get_users_text(list.users)
            markup = get_list_markup("list", list)
        return text, markup
