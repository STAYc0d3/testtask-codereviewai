from fastapi import APIRouter
from .endpoints import review

api_router = APIRouter()
api_router.include_router(review.router, tags=["review"])
