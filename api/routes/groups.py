from fastapi import APIRouter

from api.models import GroupUpdate
from database.models import Group
from ..exceptions import notfound
from ..models.group import GroupCreate

router = APIRouter(prefix="/groups")


@router.get("/")
async def _groups():
    groups = await Group.get_all()
    return [i.model_dump() for i in groups]


@router.get("/{id}")
async def _group(id: int):
    group = await Group.get(id)
    if not group:
        raise notfound
    return group.model_dump()


@router.post("/")
async def _group_create(dto: GroupCreate):
    group = await Group.create(**dto.model_dump())
    return group.model_dump()


@router.put("/{id}")
async def _group_update(id: int, dto: GroupUpdate):
    group = await Group.get(id)
    if not group:
        raise notfound

    if not dto.users:
        dto.users = group.users
    if dto.removable is None:
        dto.removable = group.removable

    group = await Group.update(id, **dto.model_dump())
    return group.model_dump()


@router.delete("/{id}")
async def _group_delete(id: int):
    await Group.delete(id)
    return {"message": "Success"}
