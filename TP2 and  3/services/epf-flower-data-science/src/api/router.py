"""API Router for FastAPI."""
from fastapi import APIRouter
from src.api.routes import authentication, data, hello, parameters

router = APIRouter()


router.include_router(hello.router, tags=["Hello"])
router.include_router(data.router, tags=["Data"], prefix="/data")
router.include_router(parameters.router, tags=["Parameters"], prefix="/parameters")