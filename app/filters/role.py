from aiogram.filters import Filter
from aiogram.types import CallbackQuery

from database.models import Group
from loader import _


class GroupRoleFilter(Filter):
    async def __call__(self, call: CallbackQuery, **data) -> bool:
        user = data['user']
        action, group_id = call.data.split("_")[-2:]
        if user.status in ("admin", "super_admin"):
            _is = True
        elif not group_id.isnumeric():
            _is = True
        elif (group := await Group.get(int(group_id))) is not None:
            _is = action in group.rules(user)
        else:
            _is = False
        if not _is:
            await call.answer(_("Not enough rights🚫"))
        return _is
