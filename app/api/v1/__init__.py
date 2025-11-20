# This file makes the v1 directory a Python package
from fastapi import APIRouter

from app.core.settings import settings

from .incidents import incidents_router

main_router = APIRouter(prefix=settings.API_V1_STR)

main_router.include_router(incidents_router)
