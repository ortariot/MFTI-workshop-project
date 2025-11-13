import uvicorn
from fastapi import FastAPI

from configs.app import settings
from api.v1.misc import router as misc_router


app = FastAPI(
    title=settings.app.app_name,
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
)


app.include_router(misc_router, prefix="/api/v1/misc", tags=["misc"])


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.app.app_host,
        port=settings.app.app_port,
    )
