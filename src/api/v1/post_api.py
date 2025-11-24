import os
from uuid import UUID, uuid4
from typing import List, Optional, Any
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    Query,
    Body,
    UploadFile,
    File,
    Form,
    BackgroundTasks,
)

import aiofiles
from services.post_service import PostService, get_post_service
from schemas.post_schema import (
    PostCreate,
    PostUpdate,
    PostResponse,
    PostWithCategoryResponse,
    PostListResponse,
    PostWithCategoryListResponse,
    PostsCountResponse,
    PostsCountByCategoryResponse,
    PostSearchParams,
    BulkAssignCategory,
)

router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("/", response_model=PostListResponse, summary="Получить посты")
async def get_all_posts(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    service: PostService = Depends(get_post_service),
):
    posts = await service.get_all_posts(skip, limit)
    total = await service.get_posts_count()

    return PostListResponse(posts=posts, total=total, skip=skip, limit=limit)


@router.get(
    "/with-category",
    response_model=PostWithCategoryListResponse,
    summary="Получить пост с указанием подрбностей о категории",
)
async def get_all_posts_with_category(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    service: PostService = Depends(get_post_service),
):
    """Получить все посты с категориями"""

    posts = await service.get_all_posts_with_category(skip, limit)
    total = await service.get_posts_count()

    return PostWithCategoryListResponse(
        posts=posts, total=total, skip=skip, limit=limit
    )


@router.get(
    "/{post_id}",
    response_model=PostResponse,
    summary="Получить пост по id",
)
async def get_post_by_id(
    post_id: Any,
    service: PostService = Depends(get_post_service),
):
    """Получить пост по id"""

    post = await service.get_post_by_id(post_id)

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )

    return post


@router.get(
    "/{post_id}/with-category",
    response_model=PostWithCategoryResponse,
    summary="Получить пост по id c указанием подрбностей о категории",
)
async def get_post_by_id_with_category(
    post_id: Any,
    service: PostService = Depends(get_post_service),
):
    """Получить пост по id с категорией"""

    post = await service.get_post_by_id_with_category(post_id)

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )

    return post


@router.get("/media/{media_id}", response_model=PostResponse)
async def get_post_by_media_id(
    media_id: str,
    service: PostService = Depends(get_post_service),
    summary="Получить пост по media_id",
):
    """Получить пост по media_id"""

    post = await service.get_post_by_media_id(media_id)

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )

    return post


async def get_post_data(
    desc: str = Form(...), category_id: UUID = Form(...)
) -> PostCreate:

    return PostCreate(desc=desc, category_id=category_id, media_id=uuid4())


@router.post(
    "/",
    response_model=PostResponse,
    status_code=status.HTTP_201_CREATED,
    summary="создать пост",
)
async def create_post(
    post_data: PostCreate = Depends(get_post_data),
    file: UploadFile = File(...),
    service: PostService = Depends(get_post_service),
):
    """Создать новый пост"""
    content = await file.read()

    if not content:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="It empty file",
        )

    # Проверка на существование media_id
    if await service.media_exists(post_data.media_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Post with this media_id already exists",
        )

    res = await service.create_post(post_data)

    with open(f"content/{res.media_id}.jpg", "wb") as f:
        f.write(content)

    return res


async def save_file_bg(contents: bytes, filename: str):

    try:

        os.makedirs("content", exist_ok=True)

        async with aiofiles.open(f"content/{filename}.jpg", "wb") as f:
            f.write(contents)
        print(f"file {filename} saved")
    except Exception as e:
        print(f"error - {e}")


@router.post(
    "/bg",
    response_model=PostResponse,
    status_code=status.HTTP_201_CREATED,
    summary="создать пост",
)
async def create_post_bg(
    post_data: PostCreate = Depends(get_post_data),
    file: UploadFile = File(...),
    service: PostService = Depends(get_post_service),
    background_task: BackgroundTasks = BackgroundTasks(),
):

    content = await file.read()

    if not content:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="It empty file",
        )

    if await service.media_exists(post_data.media_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Post with this media_id already exists",
        )

    res = await service.create_post(post_data)
    background_task.add_task(
        save_file_bg, contents=content, filename=res.media_id
    )

    return res


@router.put("/{post_id}", response_model=PostResponse, summary="обновить пост")
async def update_post(
    post_id: Any,
    update_data: PostUpdate,
    service: PostService = Depends(get_post_service),
):
    """Обновить пост"""

    # Проверка существования поста
    if not await service.post_exists(post_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )

    updated_post = await service.update_post(post_id, update_data)

    if not updated_post:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No data to update"
        )

    return updated_post


@router.delete(
    "/{post_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="удалить пост",
)
async def delete_post(
    post_id: Any,
    service: PostService = Depends(get_post_service),
):
    """Удалить пост"""

    success = await service.delete_post(post_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )


@router.post(
    "/search", response_model=PostListResponse, summary="Поиск постов по desc"
)
async def search_posts_by_description(
    search_params: PostSearchParams,
    service: PostService = Depends(get_post_service),
):
    """Поиск постов по описанию"""

    posts = await service.search_posts_by_description(
        search_params.desc_pattern, search_params.skip, search_params.limit
    )
    total = await service.get_posts_count()

    return PostListResponse(
        posts=posts,
        total=total,
        skip=search_params.skip,
        limit=search_params.limit,
    )


@router.post(
    "/search/with-category",
    response_model=PostWithCategoryListResponse,
    summary="Поиск постов по desc. Возврат с описанием категорий",
)
async def search_posts_by_description_with_category(
    search_params: PostSearchParams,
    service: PostService = Depends(get_post_service),
):
    """Поиск постов по описанию с категориями"""

    posts = await service.search_posts_by_description_with_category(
        search_params.desc_pattern, search_params.skip, search_params.limit
    )
    total = await service.get_posts_count()

    return PostWithCategoryListResponse(
        posts=posts,
        total=total,
        skip=search_params.skip,
        limit=search_params.limit,
    )


# Эндпоинты для работы с категориями
@router.get(
    "/category/{category_id}",
    response_model=PostListResponse,
    summary="Поиск постов по id категории",
)
async def get_posts_by_category_id(
    category_id: Any,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    service: PostService = Depends(get_post_service),
):
    """Получить посты по категории"""
    posts = await service.get_posts_by_category_id(category_id, skip, limit)
    total = await service.get_posts_count_by_category(category_id)

    return PostListResponse(posts=posts, total=total, skip=skip, limit=limit)


@router.get(
    "/category/{category_id}/with-category",
    response_model=PostWithCategoryListResponse,
    summary="Поиск постов по id категории с описанием категории",
)
async def get_posts_by_category_id_with_category(
    category_id: Any,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    service: PostService = Depends(get_post_service),
):
    """Получить посты по категории с информацией о категории"""

    posts = await service.get_posts_by_category_id_with_category(
        category_id, skip, limit
    )
    total = await service.get_posts_count_by_category(category_id)

    return PostWithCategoryListResponse(
        posts=posts, total=total, skip=skip, limit=limit
    )


@router.get(
    "/without-category/",
    response_model=PostListResponse,
    summary="Получить посты не принадлежащие ни одной категории",
)
async def get_posts_without_category(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    service: PostService = Depends(get_post_service),
):
    """Получить посты без категории"""

    posts = await service.get_posts_without_category(skip, limit)
    total = await service.get_posts_count()

    return PostListResponse(posts=posts, total=total, skip=skip, limit=limit)


@router.patch(
    "/{post_id}/assign-category",
    response_model=PostResponse,
    summary="назначить категорию посту",
)
async def assign_category_to_post(
    post_id: Any,
    category_id: Any = Query(..., description="ID категории"),
    service: PostService = Depends(get_post_service),
):
    """Назначить категорию посту"""

    post = await service.assign_category_to_post(post_id, category_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )

    return post


@router.patch(
    "/{post_id}/remove-category",
    response_model=PostResponse,
    summary="удалить категорию посту",
)
async def remove_category_from_post(
    post_id: Any, service: PostService = Depends(get_post_service)
):
    """Убрать категорию у поста"""

    post = await service.remove_category_from_post(post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )

    return post


# Эндпоинты для статистики
@router.get(
    "/stats/count",
    response_model=PostsCountResponse,
    summary="счётчик постов",
)
async def get_posts_count(service: PostService = Depends(get_post_service)):
    """Получить общее количество постов"""
    total = await service.get_posts_count()
    return PostsCountResponse(total=total)


@router.get(
    "/stats/count/category/{category_id}",
    response_model=PostsCountByCategoryResponse,
    summary="счётчик постов по категории",
)
async def get_posts_count_by_category(
    category_id: Any, service: PostService = Depends(get_post_service)
):
    """Получить количество постов в категории"""

    count = await service.get_posts_count_by_category(category_id)
    return PostsCountByCategoryResponse(category_id=category_id, count=count)


# Эндпоинты для пакетных операций
@router.post(
    "/bulk",
    response_model=List[PostResponse],
    status_code=status.HTTP_201_CREATED,
    summary="создать несколько постов",
)
async def create_multiple_posts(
    posts_data: List[PostCreate],
    service: PostService = Depends(get_post_service),
):
    """Создать несколько постов"""

    # Проверка на существование media_id
    for post_data in posts_data:
        if await service.media_exists(post_data.media_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Post with media_id '{post_data.media_id}' already exists",
            )

    return await service.create_multiple_posts(posts_data)


@router.post("/bulk/assign-category", summary="обновить категорию постов")
async def update_category_for_multiple_posts(
    bulk_data: BulkAssignCategory = Body(..., embed=True),
    service: PostService = Depends(get_post_service),
):
    """Обновить категорию для нескольких постов"""

    success = await service.update_category_for_multiple_posts(
        bulk_data.post_ids, bulk_data.category_id
    )

    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to update categories",
        )

    return {"message": "Categories updated successfully"}
