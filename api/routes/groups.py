from fastapi import APIRouter, Depends

from database.models import Group
from ..exceptions import notfound
from ..models import GroupUpdate, GroupCreate
from ..services import get_current_user_depends

router = APIRouter(prefix="/groups", dependencies=[Depends(get_current_user_depends)])


@router.get("/", tags=['get methods'], response_model=list[Group])
async def _groups():
    return await Group.get_all()


@router.get("/{id}", tags=['get methods'], response_model=Group)
async def _group(id: int):
    group = await Group.get(id)
    if not group:
        raise notfound
    return group


@router.post("/", tags=['post methods'], response_model=Group)
async def _group_create(dto: GroupCreate):
    group = await Group.create(**dto.model_dump())
    return group


@router.put("/{id}", tags=['put methods'], response_model=Group)
async def _group_update(id: int, dto: GroupUpdate):
    group = await Group.get(id)
    if not group:
        raise notfound

    if not dto.users:
        dto.users = group.users
    if dto.removable is None:
        dto.removable = group.removable

    return await Group.update(id, **dto.model_dump())


@router.delete("/{id}", tags=['delete methods'])
async def _group_delete(id: int):
    await Group.delete(id)
    return {"message": "Success"}
