from typing import Any, Optional

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.category import Category
from database import get_session


class CategoryRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, category_id: Any) -> Optional[Category]:
        result = await self.db.execute(
            select(Category).where(Category.uuid == category_id)
        )

        return result.scalar_one_or_none()

    async def get_by_name(self, name: str) -> Optional[Category]:
        result = await self.db.execute(select(Category).where(Category.name == name))

        return result.scalar_one_or_none()

    async def exists_by_name(self, name: str) -> bool:
        category = await self.get_by_name(name)
        return category is not None

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[Category]:
        result = await self.db.execute(select(Category).offset(skip).limit(limit))

        return result.scalars().all()

    async def create(self, category_date: dict) -> Category:
        category = Category(**category_date)
        self.db.add(category)
        await self.db.commit()
        await self.db.refresh(category)
        return category

    async def update(self, category_id: Any, category_date: dict) -> Category:
        category = await self.get_by_id(category_id)

        if category:
            for key, value in category_date.items():
                setattr(category, key, value)

            await self.db.commit()
            await self.db.refresh(category)

        return category

    async def delete(self, category_id: Any) -> bool:
        category = await self.get_by_id(category_id)

        if category:
            await self.db.delete(category)
            await self.db.commit()

            return True

        return False

    async def search_by_name(
        self, name_pattern: str, skip: int = 0, limit: int = 100
    ) -> list[Category]:
        result = await self.db.execute(
            select(Category)
            .where(Category.name.ilike(f"%{name_pattern}%"))
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()


async def get_category_reposetory(
    db: AsyncSession = Depends(get_session),
) -> CategoryRepository:
    return CategoryRepository(db)
