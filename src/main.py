import os
import uvicorn
from fastapi import FastAPI

from configs.app import settings
from api.v1.misc import router as misc_router
from api.v1.caegory_api import router as category_router
from api.v1.post_api import router as post_router
from api.v1.auth_api import router as auth_router

from cache_fastapi.cacheMiddleware import CacheMiddleware
from cache_fastapi.Backends.redis_backend import RedisBackend

os.environ["REDIS_URL"] = "redis://localhost:6379"


app = FastAPI(
    title=settings.app.app_name,
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
)

app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(misc_router, prefix="/api/v1/misc", tags=["misc"])
app.include_router(
    category_router, prefix="/api/v1/category", tags=["category"]
)
app.include_router(post_router, prefix="/api/v1/posts", tags=["posts"])


# cached_endpoints = ["/api"]
# backend = RedisBackend()
# app.add_middleware(CacheMiddleware, cached_endpoints=cached_endpoints, backend=backend)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.app.app_host,
        port=settings.app.app_port,
        reload=True,
    )
