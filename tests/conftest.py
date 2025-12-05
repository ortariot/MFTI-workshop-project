import pytest
import pytest_asyncio
import aiohttp

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from fastapi.testclient import TestClient
from src.main import app
from src.models.base import Base
from src.configs.app import settings


@pytest.fixture(scope="function")
def client():
    with TestClient(app) as client:
        yield client


@pytest_asyncio.fixture(scope="function")
async def aiohttp_client():
    session = aiohttp.ClientSession(base_url="http://localhost:8000")
    yield session
    await session.close()


@pytest_asyncio.fixture(scope="function")
async def test_engine():
    engine = create_async_engine(settings.db.dsl)

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    yield engine

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="function")
async def test_session(test_engine):

    async_session_factory = sessionmaker(
        test_engine, expire_on_commit=False, class_=AsyncSession
    )

    async with async_session_factory() as session:
        yield session
