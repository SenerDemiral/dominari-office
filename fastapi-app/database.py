# fastapi-app/database.py
import asyncpg
import redis.asyncio as redis
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:pass@db:5432/officedb")
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")

class DatabaseManager:
    def __init__(self):
        self.pool = None
        self.redis = None

    async def connect(self):
        self.pool = await asyncpg.create_pool(DATABASE_URL)
        self.redis = redis.from_url(REDIS_URL)

    async def disconnect(self):
        if self.pool: await self.pool.close()
        if self.redis: await self.redis.close()

db = DatabaseManager()