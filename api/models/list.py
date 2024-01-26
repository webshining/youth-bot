from pydantic import BaseModel


class ListUserUpdate(BaseModel):
    user_id: int
    rules: list[str]
    num: int


class ListUpdate(BaseModel):
    name: str
    removable: bool
    users: list[ListUserUpdate]
