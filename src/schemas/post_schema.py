from uuid import UUID

from typing import Optional, Any
from pydantic import BaseModel, ConfigDict

from src.schemas.category_schema import CategoryResponse


# Базовые схемы
class PostBase(BaseModel):
    media_id: UUID = None
    desc: Optional[str] = None
    category_id: UUID | None = None


# Схемы для создания и обновления
class PostCreate(PostBase):
    media_id: UUID
    desc: str


class PostUpdate(PostBase):
    pass


# Схемы для ответа
class PostResponse(PostBase):
    model_config = ConfigDict(
        from_attributes=True, exclude={"updated_at", "created_at"}
    )

    uuid: UUID


class PostWithCategoryResponse(PostResponse):
    category: Optional[CategoryResponse] = None


# Схемы для списков
class PostListResponse(BaseModel):
    posts: list[PostResponse]
    total: int
    skip: int
    limit: int


class PostWithCategoryListResponse(BaseModel):
    posts: list[PostWithCategoryResponse]
    total: int
    skip: int
    limit: int


# Схемы для статистики
class PostsCountResponse(BaseModel):
    total: int


class PostsCountByCategoryResponse(BaseModel):
    category_id: UUID
    count: int


# Схема для поиска
class PostSearchParams(BaseModel):
    desc_pattern: str
    skip: int = 0
    limit: int = 100


# Схема для пакетных операций
class BulkAssignCategory(BaseModel):
    post_ids: list[UUID]
    category_id: UUID
