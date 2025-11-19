from uuid import UUID
from fastapi import Depends, HTTPException, status

from repositories.category import CategoryRepository, get_category_reposetory
from schemas.category_schema import (
    CategoryCreate,
    CategoryResponse,
    CategoryUpdate,
)


class CategoryService:
    def __init__(self, repo):
        self.repo = repo

    async def add_category(self, in_data: CategoryCreate) -> CategoryResponse:
        if await self.check_name(in_data.name):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Категория с таким именем уже существует",
            )

        category = await self.repo.create(in_data.model_dump())
        return category

    async def check_name(self, name: str) -> CategoryResponse | None:
        return await self.repo.exists_by_name(name)

    async def get_all(self, skip: int, limit: int) -> list[CategoryResponse]:
        res = await self.repo.get_all(skip=skip, limit=limit)

        if not res:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Категориии не найдены",
            )

        return res

    async def get_by_id(self, id: UUID) -> CategoryResponse:
        res = await self.repo.get_by_id(id)

        if not res:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Категория не найдена",
            )

        return res

    async def update(self, id: UUID, in_data: CategoryUpdate) -> CategoryResponse:
        # Проверяем существование категории
        existing_category = await self.get_by_id(id)

        if in_data.name and in_data.name != existing_category.name:
            if await self.check_name(in_data.name):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Категория с таким именем уже существует",
                )

        update_dict = {k: v for k, v in in_data.model_dump().items() if v is not None}

        if update_dict:
            res = await self.repo.update(id, update_dict)
            return res

        return existing_category

    async def delete(self, id: UUID) -> None:
        res = await self.repo.delete(id)
        if not res:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Категория не найдена",
            )

    async def search_by_name(
        self, name: str, skip: int, limit: int
    ) -> CategoryResponse:
        res = await self.repo.search_by_name(name_pattern=name, skip=skip, limit=limit)

        return res


async def get_category_service(
    repo: CategoryRepository = Depends(get_category_reposetory),
) -> CategoryService:
    return CategoryService(repo)
