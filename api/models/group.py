from typing import Optional

from pydantic import BaseModel, Field


class GroupUserUpdate(BaseModel):
    user_id: int
    rules: Optional[list[str]] = Field([])
    num: Optional[int] = Field(0)


class GroupUpdate(BaseModel):
    name: str
    removable: bool
    users: list[GroupUserUpdate]
