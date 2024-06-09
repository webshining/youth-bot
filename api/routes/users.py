from fastapi import APIRouter, Depends

from database.models import User
from ..exceptions import notfound
from ..models import UserUpdate
from ..services import get_current_user_depends

router = APIRouter(prefix="/users", dependencies=[Depends(get_current_user_depends)])


@router.get("/", tags=['get methods'], response_model=list[User])
async def _users():
    return await User.get_all()


@router.get("/{id}", tags=['get methods'], response_model=User)
async def _user(id: int):
    if user := await User.get(id):
        return user
    raise notfound


@router.put("/{id}", tags=['put methods'], response_model=User)
async def _user_update(id: int, dto: UserUpdate):
    user = await User.get(id)
    if not user:
        raise notfound
    user = await User.update(id, **dto.model_dump())
    return user
