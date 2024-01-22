from pydantic import Field, BaseModel

from loader import db
from .base import Base
from .user import User


class ListUser(BaseModel):
    user: User
    rules: list[str] = Field(default=[""])


class List(Base):
    id: int = Field(default_factory=int, alias="_id")
    name: str
    users: list[ListUser] = Field(default=[])

    _rules: list[str] = ["read", "edit", "delete", "send"]

    def rules(self, user: User) -> list[str]:
        _user = next((i for i in self.users if i.user.id == user.id), None)
        if user.status in ("admin", "super_admin"):
            return self._rules
        if not _user:
            return []
        return _user.rules

    @classmethod
    async def get(cls, id: int):
        obj = await cls._collection.aggregate([
            {"$match": {"_id": id}},
            {"$unwind": {"path": "$users", "preserveNullAndEmptyArrays": True}},
            {"$lookup": {"from": "users", "localField": "users.user_id", "foreignField": "_id", "as": "users.user"}},
            {"$unwind": {"path": "$users.user", "preserveNullAndEmptyArrays": True}},
            {"$group": {"_id": "$_id", "users": {"$push": "$users"}, "name": {"$first": "$name"}}},
            {"$project": {"users": {"$cond": {"if": {"$eq": ["$users", [{}]]}, "then": [], "else": "$users"}},
                          "name": "$name"}}
        ]).to_list(length=1000)
        return cls(**obj[0]) if obj else None

    @classmethod
    async def get_all(cls):
        objs = await cls._collection.aggregate([
            {"$unwind": {"path": "$users", "preserveNullAndEmptyArrays": True}},
            {"$lookup": {"from": "users", "localField": "users.user_id", "foreignField": "_id", "as": "users.user"}},
            {"$unwind": {"path": "$users.user", "preserveNullAndEmptyArrays": True}},
            {"$group": {"_id": "$_id", "users": {"$push": "$users"}, "name": {"$first": "$name"}}},
            {"$project": {"users": {"$cond": {"if": {"$eq": ["$users", [{}]]}, "then": [], "else": "$users"}},
                          "name": "$name"}}
        ]).to_list(length=1000)
        return [cls(**u) for u in objs]


List.set_collection(db['lists'])
