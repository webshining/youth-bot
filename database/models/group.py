from pydantic import Field, BaseModel

from .base import Base, execute
from .user import User


class GroupUser(BaseModel):
    user: User
    rules: list[str] = Field(default=[])
    num: int


class Group(Base):
    id: str
    name: str
    users: list[GroupUser] = Field(default=[])
    removable: bool = Field(default=True)

    _rules: list[str] = ["read", "edit", "delete", "send", "users"]

    def rules(self, user: User) -> list[str]:
        if user.status in ("admin", "super_admin"):
            return self._rules
        _user = next((i for i in self.users if i.user.id == user.id), None)
        if not _user:
            return []
        return _user.rules

    @execute
    async def get(cls, id: int | str, session=None):
        query = await session.query(f"SELECT * FROM {cls._table}:{id} FETCH users.user")
        obj = next(iter(query[0]['result']), None)
        obj = cls(**obj) if obj else obj
        if obj:
            obj.users = sorted(obj.users, key=lambda u: u.num)
        return obj

    @execute
    async def get_all(cls, session=None):
        objs = await session.select(cls._table)
        for o in objs:
            o['users'] = []
        return [cls(**o) for o in objs]


Group.set_collection('group')
