from fastapi import APIRouter

from database.models import User
from ..exceptions import notfound
from ..models import UserUpdate

router = APIRouter(prefix="/users")


@router.get("/")
async def _users():
    users = await User.get_all()
    return [i.model_dump() for i in users]


@router.get("/{id}")
async def _user(id: int):
    user = await User.get(id)
    if not user:
        raise notfound
    return user.model_dump()


@router.put("/{id}")
async def _user_update(id: int, dto: UserUpdate):
    user = await User.get(id)
    if not user:
        raise notfound
    user = await User.update(id, **dto.model_dump())
    return user.model_dump()
