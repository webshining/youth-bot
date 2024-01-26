from fastapi import APIRouter, Request

from .auth import router as auth_router
from .lists import router as lists_router
from .users import router as users_router

router = APIRouter()


@router.get("/ping")
async def _ping(request: Request):
    print(request.url_for("_auth_redirect"))
    return {"message": "ok"}


router.include_router(users_router)
router.include_router(lists_router)
router.include_router(auth_router)
