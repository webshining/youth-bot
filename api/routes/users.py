from fastapi import APIRouter, Depends

from database.models import User

from ..services import get_current_user, notfound

router = APIRouter(prefix="/users", dependencies=[Depends(get_current_user)])


@router.get("/")
async def _users():
    users = await User.get_all()
    return [i.model_dump() for i in users]


@router.get("/{id}")
async def _user(id: int):
    user = await User.get(id)
    return user.model_dump() if user else {"error": notfound}
