from fastapi import APIRouter, Depends

from api.models import GroupUpdate
from api.services import get_current_user, notfound
from database.models import Group

router = APIRouter(prefix="/groups", dependencies=[Depends(get_current_user)])


@router.get("/")
async def _groups():
    groups = await Group.get_all()
    return [i.model_dump() for i in groups]


@router.get("/{id}")
async def _group(id: int):
    group = await Group.get(id)
    return group.model_dump() if group else {"error": notfound.detail}


@router.put("/{id}")
async def _group_put(id: int, dto: GroupUpdate):
    group = await Group.get(id)
    if not group:
        return {"error": notfound.detail}
    for i, u in enumerate(dto.users):
        u.num = i + 1
    await Group.update(id, **dto.model_dump())
