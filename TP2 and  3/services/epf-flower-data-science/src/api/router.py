"""API Router for FastAPI."""
from fastapi import APIRouter
from src.api.routes import hello, data  # Import the new data router

router = APIRouter()

# Include existing routes
router.include_router(hello.router, tags=["Hello"])

# Include new data routes
router.include_router(data.router, tags=["Data"], prefix="/data")
