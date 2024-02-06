from aiogram import F, html
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from app.keyboards import get_apply_markup
from app.routers import user_router as router
from app.states import NeedState
from database.models import Need
from loader import _


@router.message(Command("need"))
async def _need(message: Message, state: FSMContext):
    await message.answer(_("Enter your name:"))
    await state.set_state(NeedState.name)


@router.message(F.text, NeedState.name)
async def _need_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer(_("Enter your need:"))
    await state.set_state(NeedState.text)


@router.message(F.text, NeedState.text)
async def _need_text(message: Message, state: FSMContext):
    data = await state.get_data()
    text = f'<blockquote>{html.quote(data.get("name"))}</blockquote>\n{html.quote(message.text)}'
    await message.answer(text=text, reply_markup=get_apply_markup("need"))
    await message.delete()
    await state.set_state(None)


@router.callback_query(lambda call: call.data.startswith("need"))
async def _need_apply(call: CallbackQuery):
    await Need.create(text=call.message.html_text)
    await call.message.edit_reply_markup(reply_markup=None)
    await call.answer(_("Success"))
