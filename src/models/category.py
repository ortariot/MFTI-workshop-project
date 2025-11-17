import uuid
import asyncio
from typing import Any

from sqlalchemy import Column, String, Text
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.models.base import Base, BaseModelMixin
from src.configs.app import settings


class Category(Base, BaseModelMixin):

    __tablename__ = "category"

    name = Column(String, nullable=False, unique=True)
    desc = Column(Text)

    posts = relationship("Posts", backref="category_ref", lazy="select")


    def __repr__(self) -> str:
        return f"uuid - {self.uuid}, name - {self.name} desc - {self.desc}"

    def to_dict(self) -> dict[str, Any]:
        return {
            "uuid": self.uuid,
            "name": self.name,
            "desc": self.desc,
        }


async def create_db():

    engine = create_async_engine("postgresql+asyncpg://user:password@localhost:5432/postgres")

    async with engine.begin() as connection:
        pass
        # await connection.run_sync(Base.metadata.drop_all)
        # await connection.run_sync(Base.metadata.create_all)


if __name__ == "__main__":

    asyncio.run(create_db())
