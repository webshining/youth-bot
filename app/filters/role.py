from aiogram.filters import Filter
from aiogram.types import CallbackQuery

from database.models import List
from loader import _


class ListRoleFilter(Filter):
    async def __call__(self, call: CallbackQuery, **data) -> bool:
        user = data['user']
        action, list_id = call.data.split("_")[-2:]
        if user.status == "admin":
            _is = True
            await data['state'].update_data(rules=["delete", "edit", "send"])
        elif not list_id.isnumeric():
            _is = True
        elif (item := await List.get(int(list_id))) is not None:
            _is = action in item.rules(user.id)
        else:
            _is = False
        if not _is:
            await call.answer(_("Not enough rights🚫"))
        return _is