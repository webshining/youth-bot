from typing import Optional

from fastapi import Query
from pydantic import BaseModel, Field


class ListUserUpdate(BaseModel):
    user_id: int
    rules: Optional[list[str]] = Field([])
    num: Optional[int] = Field(0)


class ListUpdate(BaseModel):
    name: str
    removable: bool
    users: list[ListUserUpdate]
