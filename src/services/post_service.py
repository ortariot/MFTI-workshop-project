from typing import List, Optional, Any

from fastapi import Depends
from src.repositories.posts import PostRepository, get_post_reposetory

from src.schemas.post_schema import (
    PostCreate,
    PostUpdate,
    PostResponse,
    PostWithCategoryResponse,
)


class PostService:
    def __init__(self, repo: PostRepository):
        self.repo = repo

    async def get_post_by_id(self, post_id: Any) -> Optional[PostResponse]:
        """Получить пост по ID"""
        post = await self.repo.get_by_id(post_id)
        return post

    async def get_post_by_id_with_category(
        self, post_id: Any
    ) -> Optional[PostWithCategoryResponse]:
        """Получить пост по ID с информацией о категории"""
        post = await self.repo.get_by_id_with_category(post_id)
        return post

    async def get_post_by_media_id(
        self, media_id: Any
    ) -> Optional[PostResponse]:
        """Получить пост по media_id"""
        post = await self.repo.get_by_media_id(media_id)
        return post

    async def get_all_posts(
        self, skip: int = 0, limit: int = 100
    ) -> List[PostResponse]:
        """Получить все посты"""
        posts = await self.repo.get_all(skip, limit)
        return [post for post in posts]

    async def get_all_posts_with_category(
        self, skip: int = 0, limit: int = 100
    ) -> List[PostWithCategoryResponse]:
        """Получить все посты с категориями"""
        posts = await self.repo.get_all_with_category(skip, limit)
        return [post for post in posts]

    async def create_post(self, post_data: PostCreate) -> PostResponse:
        """Создать новый пост"""
        post_dict = post_data.model_dump()
        post = await self.repo.create(post_dict)
        return post

    async def update_post(
        self, post_id: Any, update_data: PostUpdate
    ) -> Optional[PostResponse]:
        """Обновить пост"""
        # Удаляем None значения для частичного обновления
        update_dict = {
            k: v for k, v in update_data.model_dump().items() if v is not None
        }

        if not update_dict:
            return None

        post = await self.repo.update(post_id, update_dict)
        return post

    async def delete_post(self, post_id: Any) -> bool:
        """Удалить пост"""
        return await self.repo.delete(post_id)

    async def search_posts_by_description(
        self, desc_pattern: str, skip: int = 0, limit: int = 100
    ) -> List[PostResponse]:
        """Поиск постов по описанию"""
        posts = await self.repo.search_by_description(
            desc_pattern, skip, limit
        )
        return [post for post in posts]

    async def search_posts_by_description_with_category(
        self, desc_pattern: str, skip: int = 0, limit: int = 100
    ) -> List[PostWithCategoryResponse]:
        """Поиск постов по описанию с категориями"""
        posts = await self.repo.search_by_description_with_category(
            desc_pattern, skip, limit
        )
        return [post for post in posts]

    # Работа с категориями
    async def get_posts_by_category_id(
        self, category_id: Any, skip: int = 0, limit: int = 100
    ) -> List[PostResponse]:
        """Получить посты по категории"""
        posts = await self.repo.get_by_category_id(category_id, skip, limit)
        return [post for post in posts]

    async def get_posts_by_category_id_with_category(
        self, category_id: Any, skip: int = 0, limit: int = 100
    ) -> List[PostWithCategoryResponse]:
        """Получить посты по категории с информацией о категории"""
        posts = await self.repo.get_by_category_id_with_category(
            category_id, skip, limit
        )
        return [post for post in posts]

    async def get_posts_without_category(
        self, skip: int = 0, limit: int = 100
    ) -> List[PostResponse]:
        """Получить посты без категории"""
        posts = await self.repo.get_posts_without_category(skip, limit)
        return [post for post in posts]

    async def assign_category_to_post(
        self, post_id: Any, category_id: Any
    ) -> Optional[PostResponse]:
        """Назначить категорию посту"""
        post = await self.repo.assign_category(post_id, category_id)
        return post

    async def remove_category_from_post(
        self, post_id: Any
    ) -> Optional[PostResponse]:
        """Убрать категорию у поста"""
        post = await self.repo.remove_category(post_id)
        return post

    # Проверки
    async def post_exists(self, post_id: Any) -> bool:
        """Проверить существование поста"""
        return await self.repo.exists_by_id(post_id)

    async def media_exists(self, media_id: Any) -> bool:
        """Проверить существование media_id"""
        return await self.repo.exists_by_media_id(media_id)

    # Статистика
    async def get_posts_count(self) -> int:
        """Получить общее количество постов"""
        return await self.repo.get_count()

    async def get_posts_count_by_category(self, category_id: Any) -> int:
        """Получить количество постов в категории"""
        return await self.repo.get_count_by_category(category_id)

    # Пакетные операции
    async def create_multiple_posts(
        self, posts_data: List[PostCreate]
    ) -> List[PostResponse]:
        """Создать несколько постов"""
        posts_dict = [post_data.model_dump for post_data in posts_data]
        posts = await self.repo.create_many(posts_dict)
        return [post for post in posts]

    async def update_category_for_multiple_posts(
        self, post_ids: List[Any], category_id: Any
    ) -> bool:
        """Обновить категорию для нескольких постов"""

        return await self.repo.update_category_for_posts(post_ids, category_id)


async def get_post_service(
    repo: PostRepository = Depends(get_post_reposetory),
) -> PostService:
    return PostService(repo)
