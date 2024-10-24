from fastapi import APIRouter

from ..internal.admin import router as admin_router
from .auth import router as auth_router
from .chart_analysis import router as chart_analysis_router

router = APIRouter(prefix="/api")   
router.include_router(auth_router)
router.include_router(chart_analysis_router)
router.include_router(admin_router)
