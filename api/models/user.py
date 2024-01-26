from pydantic import BaseModel


class UserUpdate(BaseModel):
    status: str
