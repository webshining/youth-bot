from enum import Enum

from pydantic import Field

from .base import Base


class Status(Enum):
    banned = 0
    user = 1
    admin = 2
    super_admin = 3


class User(Base):
    id: int
    name: str
    username: str | None = Field(default=None)
    status: str = Field(default="user")
    lang: str = Field(default="en")
    notifications: bool = Field(default=True)

    _status: Status = Status

    def is_admin(self, super: bool = False) -> bool:
        if super:
            return self.status == "super_admin"
        return self.status in ("admin", "super_admin")

    def statuses_to_edit(self, status: str) -> list[str]:
        self_status = getattr(self._status, self.status).value
        status = getattr(self._status, status).value
        return [] if status >= self_status else [i.name for i in self._status if i.value < self_status]


User.set_collection('user')
