from pydantic import Field, BaseModel

from .base import Base
from .user import User


class GroupUser(BaseModel):
    user: User
    rules: list[str] = Field(default=[""])
    num: int


_aggregate_params: list[dict] = [
    {"$unwind": {"path": "$users", "preserveNullAndEmptyArrays": True}},
    {"$lookup": {"from": "users", "localField": "users.user_id", "foreignField": "_id", "as": "users.user"}},
    {"$unwind": {"path": "$users.user", "preserveNullAndEmptyArrays": True}},
    {"$group": {"_id": "$_id", "name": {"$first": "$name"}, "users": {"$push": "$users"},
                "removable": {"$first": "$removable"}}},
    {"$project": {"removable": "$removable", "name": "$name",
                  "users": {"$sortArray": {
                      "input": {"$cond": {"if": {"$eq": ["$users", [{}]]}, "then": [], "else": "$users"}},
                      "sortBy": {"num": 1}}}}},
]


class Group(Base):
    id: int = Field(default_factory=int, alias="_id")
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

    @classmethod
    async def get(cls, id: int):
        obj = await cls._collection.aggregate([
            {"$match": {"_id": id}},
            *_aggregate_params
        ]).to_list(length=1)
        return cls(**obj[0]) if obj else None

    @classmethod
    async def get_all(cls):
        objs = await cls._collection.aggregate([
            *_aggregate_params
        ]).to_list(length=1000)
        return [cls(**u) for u in objs]


Group.set_collection('groups')
