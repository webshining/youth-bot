from pydantic import Field

from loader import db
from .base import Base
from .status import Status


class User(Base):
    id: int = Field(default_factory=int, alias="_id")
    name: str
    username: str | None = Field(default=None)
    status: str = Field(default="user")
    lang: str

    _status: Status = Status

    def is_admin(self, super: bool = False) -> bool:
        if super:
            return self.status in ("super_admin",)
        return self.status in ("admin", "super_admin")

    def statuses_to_edit(self, status: str) -> list[str]:
        self_status = getattr(self._status, self.status).value
        status = getattr(self._status, status).value
        return [] if status >= self_status else [i.name for i in self._status if i.value < self_status]

    @classmethod
    async def get_or_create(cls, id: int, name: str, username: str | None, lang: str):
        user = await cls.get(id)
        data = {"username": username}
        if not user:
            data['_id'] = id
            data['name'] = name
            data['lang'] = lang
        user = await cls.update(user.id, **data) if user else await cls.create(**data)
        return user


User.set_collection(db['users'])
