from pydantic import Field

from loader import db
from .base import Base
from .status import Status


class User(Base):
    id: int = Field(default_factory=int, alias="_id")
    name: str
    username: str | None
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
    async def get_or_create(cls, id: int, **kwargs):
        user = await cls.get(id)
        if not user:
            kwargs['_id'] = id
            kwargs['status'] = "user"
        user = user or await cls.create(**kwargs)
        return user


User.set_collection(db['users'])
