from fastapi import APIRouter

from .register import router as register_router
from .basic import router as basic_auth_router


router = APIRouter(prefix="/auth", tags=["Auth"])

router.include_router(register_router)
router.include_router(basic_auth_router)