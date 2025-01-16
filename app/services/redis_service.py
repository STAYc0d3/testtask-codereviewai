import aioredis
from app.core.config import get_settings

class RedisService:
    def __init__(self):
        self.settings = get_settings()
        self.redis = None

    async def connect(self):
        self.redis = await aioredis.from_url(
            f"redis://{self.settings.REDIS_HOST}:{self.settings.REDIS_PORT}",
            password=self.settings.REDIS_PASSWORD,
            decode_responses=True
        )

    async def disconnect(self):
        if self.redis:
            await self.redis.close()

    async def set(self, key: str, value: str, expire: int = None):
        await self.redis.set(key, value, ex=expire)

    async def get(self, key: str):
        return await self.redis.get(key)

    async def delete(self, key: str):
        await self.redis.delete(key)
