from .groups import router as admin_router
from .needs import router as admin_router
from .notify import router as super_admin_router
from .users import router as super_admin_router

__all__ = [
    'admin_router', "super_admin_router"
]
