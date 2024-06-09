from aiogram import F, html
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app.filters import GroupRoleFilter
from app.keyboards import (get_apply_markup, get_groups_markup, get_group_markup)
from app.routers import user_router as router
from app.states import GroupState
from database.models import Group, User
from loader import _
from ..admins.users import _get_users_text


@router.message(Command('groups'))
async def _groups(message: Message, user: User):
    text, markup = await _get_groups_data(user)
    await message.answer(text, reply_markup=markup)


@router.callback_query(lambda call: call.data.startswith('groups') and call.data != "groups_create", GroupRoleFilter())
async def _groups_call(call: CallbackQuery, user: User):
    if call.data[7:] == 'refresh':
        text, markup = await _get_groups_data(user)
    else:
        group = await Group.get(call.data[12:])
        text, markup = await _get_group_data(group, user)

    try:
        await call.message.edit_text(text, reply_markup=markup)
    except:
        pass
    await call.answer()


@router.callback_query(lambda call: call.data.startswith('group_'), GroupRoleFilter())
async def _group(call: CallbackQuery, state: FSMContext, user: User):
    if call.data[6:] == 'back':
        text, markup = await _get_groups_data(user)
    else:
        if (group := await Group.get(call.data.split("_")[-1])) is not None:
            if call.data[6:].startswith('delete'):
                text, markup = (_("Do you really want to delete the group <b>{}</b>?").format(html.quote(group.name)),
                                get_apply_markup("apply", "group", "delete", group.id))
                await call.message.edit_text(text, reply_markup=markup)
            elif call.data[6:].startswith('edit'):
                text, markup = _("Enter new name:"), None
                await state.set_state(GroupState.edit_name)
            elif call.data[6:].startswith('send'):
                text, markup = _("Enter message text:"), None
                await state.set_state(GroupState.send_message)
            else:
                text, markup = await _get_groups_data(user)
            await state.update_data(group_id=group.id)
        else:
            text, markup = await _get_groups_data(user)

    try:
        await call.message.edit_text(text, reply_markup=markup)
    except:
        pass
    await call.answer()


@router.callback_query(lambda call: call.data.startswith('apply_group'), GroupRoleFilter())
async def _group_apply(call: CallbackQuery, state: FSMContext, user: User):
    if (group := await Group.get(call.data.split('_')[-1])) is not None:
        if call.data[12:].startswith('delete'):
            await Group.delete(group.id)
            text, markup = await _get_groups_data(user)
        elif call.data[12:].startswith('edit'):
            data = await state.get_data()
            if (group_name := data.get('group_name')) is not None:
                await Group.update(group.id, name=group_name)
            text, markup = await _get_groups_data(user)
        elif call.data[12:].startswith("send"):
            for i in group.users:
                if i.user.id != call.from_user.id:
                    try:
                        await call.message.copy_to(chat_id=i.user.id, reply_markup=None)
                    except:
                        pass

            text, markup = await _get_groups_data(user)
            await call.message.delete()
            return await call.message.answer(text, reply_markup=markup)
        else:
            text, markup = await _get_groups_data(user)
    else:
        text, markup = await _get_groups_data(user)

    try:
        await call.message.edit_text(text, reply_markup=markup)
    except:
        pass
    await call.answer()


@router.message(GroupState.send_message)
async def _group_send(message: Message, state: FSMContext, user: User):
    data = await state.get_data()
    if (group_id := data.get('group_id')) is not None and await Group.get(group_id):
        markup = get_apply_markup("apply", "group", "send", group_id)
        await message.copy_to(chat_id=message.chat.id, reply_markup=markup)
    else:
        text, markup = await _get_groups_data(user)
        await message.answer(text, reply_markup=markup)

    await state.set_state(None)


@router.message(GroupState.edit_name, F.text)
async def _group_edit(message: Message, state: FSMContext, user: User):
    data = await state.get_data()
    if (group_id := data.get('group_id')) is not None and (group := await Group.get(group_id)) is not None:
        text, markup = (
            _("Do you really want to change the group name from <b>{}</b> to <b>{}</b>?").format(html.quote(group.name),
                                                                                                 html.quote(
                                                                                                     message.text)),
            get_apply_markup("apply", "group", "edit", group_id))
        await state.update_data(group_name=message.text)
    else:
        text, markup = await _get_groups_data(user)

    await message.answer(text, reply_markup=markup)
    await state.set_state(None)


async def _get_group_data(group: Group | None, user: User):
    if not group:
        text, markup = await _get_groups_data(user)
    else:
        text = f"<b>{html.quote(group.name)}:</b>"
        text += _get_users_text([u.user for u in group.users])
        markup = get_group_markup(group, user)
    return text, markup


async def _get_groups_data(user: User):
    text = _("Select group:")
    markup = get_groups_markup(await Group.get_all(), user)
    return text, markup
