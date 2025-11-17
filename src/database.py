from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from configs import settings


engine = create_async_engine(settings.db.dsl, echo=True)

async_sesion_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_sesion_maker() as session:
        try:
            yield session
        finally:
            await session.close()
