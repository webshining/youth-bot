from fastapi import APIRouter, Depends

from api.models import ListUpdate
from api.services import get_current_user, notfound
from database.models import List

router = APIRouter(prefix="/lists", dependencies=[Depends(get_current_user)])


@router.get("/")
async def _lists():
    lists = await List.get_all()
    return [i.model_dump() for i in lists]


@router.get("/{id}")
async def _user(id: int):
    list = await List.get(id)
    return list.model_dump() if list else {"error": notfound}


@router.put("/{id}")
async def _list_put(id: int, dto: ListUpdate):
    list = await List.get(id)
    if not list:
        return {"error": notfound.detail}
    for i, u in enumerate(dto.users):
        u.num = i+1
    await List.update(id, **dto.model_dump())
