import asyncio

from redis.asyncio import Redis
from configs.app import settings


class Cache:

    def __init__(self, host, port):

        self.cache = Redis(host=host, port=port)

    async def add(self, key=None, value=None, expire=None, **kwargs):
        if key and value:
            await self.cache.set(key, value, expire)
        elif kwargs:
            for key, value in kwargs.items():
                await self.cache.set(key, value, expire)

    async def get(self, key: str, **kwargs):
        data = await self.cache.get(key)
        return data

    async def delete(self, key: str) -> None:

        await self.cache.delete(key)


async def get_cache() -> Cache:
    return Cache(settings.cache.cache_host, settings.cache.cache_port)


cache = Cache("localhost", 6379)


async def runner(cache):
    await cache.add(**{"a": "hello", "b": "world"})

    res = await cache.get("a")
    print(res)


if __name__ == "__main__":
    cache = Cache(settings.cache.cache_host, settings.cache.cache_port)

    asyncio.run(runner(cache))
