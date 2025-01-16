import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api import api_router
from app.services.redis_service import RedisService

redis_service = RedisService()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await redis_service.connect()
    yield
    # Shutdown
    await redis_service.disconnect()

app = FastAPI(
    title="CodeReviewAI",
    description="AI-powered code review tool for analyzing GitHub repositories",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(api_router, prefix="/api/v1")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 