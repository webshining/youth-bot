from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from app.filters import ListRoleFilter
from app.keyboards import get_lists_markup, get_list_markup, get_apply_markup
from app.routers import user_router as router
from app.states import ListState
from database.models import List, User
from loader import _
from ..admins.users import _get_users_text


@router.message(Command('lists'))
async def _lists(message: Message, user: User):
    text, markup = await _get_lists_data(user.is_admin())
    await message.answer(text, reply_markup=markup)


@router.callback_query(lambda call: call.data.startswith('lists'), ListRoleFilter())
async def _lists_call(call: CallbackQuery, user: User):
    if call.data[6:] == 'refresh':
        text, markup = await _get_lists_data(user.is_admin())
    else:
        list = await List.get(int(call.data[11:]))
        text, markup = await _get_list_data(list, user)

    try:
        await call.message.edit_text(text, reply_markup=markup)
    except:
        pass
    await call.answer()


@router.callback_query(lambda call: call.data.startswith('list'), ListRoleFilter())
async def _list(call: CallbackQuery, state: FSMContext, user: User):
    if call.data[5:] == 'back':
        text, markup = await _get_lists_data(user.is_admin())
    else:
        if (item := await List.get(int(call.data.split("_")[-1]))) is not None:
            if call.data[5:].startswith('delete'):
                text, markup = (_("Do you really want to delete the list <b>{}</b>?").format(item.name),
                                get_apply_markup("apply", "list", "delete", item.id))
                await call.message.edit_text(text, reply_markup=markup)
            elif call.data[5:].startswith('edit'):
                text, markup = _("Enter new name:"), None
                await state.set_state(ListState.edit_name)
            elif call.data[5:].startswith('send'):
                text, markup = _("Enter message text:"), None
                await state.set_state(ListState.send_message)
            else:
                text, markup = await _get_lists_data(user.is_admin())
            await state.update_data(list_id=item.id)
        else:
            text, markup = await _get_lists_data(user.is_admin())

    try:
        await call.message.edit_text(text, reply_markup=markup)
    except:
        pass
    await call.answer()


@router.callback_query(lambda call: call.data.startswith('apply_list'), ListRoleFilter())
async def _list_apply(call: CallbackQuery, state: FSMContext, user: User):
    if (item := await List.get(int(call.data.split('_')[-1]))) is not None:
        if call.data[11:].startswith('delete'):
            await List.delete(item.id)
            text, markup = await _get_lists_data(user.is_admin())
        elif call.data[11:].startswith('edit'):
            data = await state.get_data()
            if (list_name := data.get('list_name')) is not None:
                await List.update(item.id, name=list_name)
            text, markup = await _get_lists_data(user.is_admin())
        elif call.data[11:].startswith("send"):
            for i in item.users:
                if i.user.id != call.from_user.id:
                    await call.message.copy_to(chat_id=i.user.id, reply_markup=None)

            text, markup = await _get_lists_data(user.is_admin())
            await call.message.delete()
            return await call.message.answer(text, reply_markup=markup)
        else:
            text, markup = await _get_lists_data(user.is_admin())
    else:
        text, markup = await _get_lists_data(user.is_admin())

    try:
        await call.message.edit_text(text, reply_markup=markup)
    except:
        pass
    await call.answer()


@router.message(ListState.send_message)
async def _list_send(message: Message, state: FSMContext, user: User):
    data = await state.get_data()
    if (list_id := data.get('list_id')) is not None and await List.get(int(list_id)):
        markup = get_apply_markup("apply", "list", "send", list_id)
        await message.copy_to(chat_id=message.chat.id, reply_markup=markup)
    else:
        text, markup = await _get_lists_data(user.is_admin())
        await message.answer(text, reply_markup=markup)

    await state.set_state(None)


@router.message(ListState.edit_name)
async def _list_edit(message: Message, state: FSMContext, user: User):
    data = await state.get_data()
    if (list_id := data.get('list_id')) is not None and (item := await List.get(int(list_id))) is not None:
        text, markup = (
            _("Do you really want to change the list name from <b>{}</b> to <b>{}</b>?").format(item.name,
                                                                                                message.text),
            get_apply_markup("apply", "list", "edit", list_id))
        await state.update_data(list_name=message.text)
    else:
        text, markup = await _get_lists_data(user.is_admin())

    await message.answer(text, reply_markup=markup)
    await state.set_state(None)


async def _get_list_data(list: List | None, user: User):
    if not list:
        text, markup = await _get_lists_data(user.is_admin())
    else:
        text = f"<b>{list.name}:</b>"
        text += _get_users_text([u.user for u in list.users])
        markup = get_list_markup(list.id, list.rules(user.id))
    return text, markup


async def _get_lists_data(is_admin: bool = False):
    text = _("Select list:")
    markup = get_lists_markup(await List.get_all(), is_admin)
    return text, markup
