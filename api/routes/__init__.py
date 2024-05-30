from fastapi import APIRouter

from .auth import router as auth_router
from .groups import router as groups_router
from .users import router as users_router

router = APIRouter(prefix="/api")


@router.get("/ping")
async def _ping():
    return {"message": "ok"}


router.include_router(users_router, tags=['users'])
router.include_router(groups_router, tags=['groups'])
router.include_router(auth_router, tags=['auth'])
