from typing import List, Optional
from fastapi import APIRouter, Depends, status, Query


from schemas.category_schema import (
    CategoryResponse,
    CategoryCreate,
    CategoryUpdate,
)
from services.category_service import get_category_service, CategoryService
from services.auth_service import get_auth_service, AuthService

router = APIRouter()


# Эндпоинты
@router.post(
    "/",
    response_model=CategoryResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Создать категорию",
)
async def create_category(
    category_data: CategoryCreate,
    service: CategoryService = Depends(get_category_service),
    # repository: CategoryRepository = Depends(get_category_repository)
    auth: AuthService = Depends(get_auth_service)
):
    """
    Создать новую категорию
    """

    # if await repository.exists_by_name(category_data.name):
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail="Категория с таким именем уже существует"
    #     )

    # category = await repository.create(category_data.dict())
    # return category
    auth.get_current_user()
    res = await service.add_category(category_data)
    return res


@router.get(
    "/",
    response_model=List[CategoryResponse],
    summary="Получить все категории",
)
async def get_all_categories(
    skip: int = Query(0, ge=0, description="Количество записей для пропуска"),
    limit: int = Query(100, ge=1, le=1000, description="Лимит записей"),
    service: CategoryService = Depends(get_category_service),
    auth: AuthService = Depends(get_auth_service)
):
    """
    Получить список всех категорий с пагинацией
    """

    auth.get_current_user()
    categories = await service.get_all(skip=skip, limit=limit)
    return categories


@router.get(
    "/{category_id}",
    response_model=CategoryResponse,
    summary="Получить категорию по ID",
)
async def get_category(
    category_id: str, service: CategoryService = Depends(get_category_service)
):
    """
    Получить категорию по идентификатору
    """
    category = await service.get_by_id(category_id)

    return category


@router.put(
    "/{category_id}",
    response_model=CategoryResponse,
    summary="Обновить категорию",
)
async def update_category(
    category_id: str,
    update_data: CategoryUpdate,
    service: CategoryService = Depends(get_category_service),
):
    """
    Обновить данные категории
    """

    category = await service.update(category_id, update_data)

    return category


@router.delete(
    "/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить категорию",
)
async def delete_category(
    category_id: str, service: CategoryService = Depends(get_category_service)
):
    """
    Удалить категорию
    """
    await service.delete(category_id)


@router.get(
    "/search/",
    response_model=List[CategoryResponse],
    summary="Поиск категорий по имени",
)
async def search_categories(
    name: str = Query(..., description="Шаблон для поиска по имени"),
    skip: int = Query(0, ge=0, description="Количество записей для пропуска"),
    limit: int = Query(100, ge=1, le=1000, description="Лимит записей"),
    service: CategoryService = Depends(get_category_service),
):
    """
    Поиск категорий по шаблону имени (регистронезависимый)
    """
    categories = await service.search_by_name(name=name, skip=skip, limit=limit)
    return categories


@router.get("/check/{name}", summary="Проверить существование категории по имени")
async def check_category_exists(
    name: str, service: CategoryService = Depends(get_category_service)
):
    """
    Проверить, существует ли категория с указанным именем
    """
    exists = await service.check_name(name)
    return {"exists": exists}
