from typing import Optional

from pydantic import BaseModel, Field


class GroupUser(BaseModel):
    user_id: int
    rules: Optional[list[str]] = Field([])
    num: Optional[int] = Field(1)


class GroupCreate(BaseModel):
    name: str
    removable: bool = Field(True)
    users: list[GroupUser] = Field([])


class GroupUpdate(BaseModel):
    name: str
    removable: bool | None = Field(None)
    users: list[GroupUser] | None = Field(None)
