from typing import List, Optional, Any

from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status

from repositories.user import UserRepository, get_user_reposetory
from schemas.user_schema import UserResponse, UserRegistrate


class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo
        self.pwd_context = CryptContext(schemes=["sha512_crypt"])

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)

    async def get_user_by_id(self, user_id: Any) -> UserResponse | None:
        """Получить пользователя по ID"""
        user = await self.repo.get_by_id(user_id)
        return user

    async def get_user_by_name(self, username: str) -> UserResponse | None:
        """Получить пользователя по имни"""
        post = await self.repo.get_by_name(username)
        return post

    async def get_user_by_email(self, email: str) -> UserResponse | None:
        """Получить пользователя по имни"""
        post = await self.repo.get_by_name(email)
        return post

    async def create_user(self, user_data: UserRegistrate) -> UserResponse:
        """Создать нового пользователя"""
        if await self.get_user_by_email(user_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Пользователь уже существует",
            )

        data_dump = user_data.model_dump()
        data_dump["hashed_password"] = self.get_password_hash(
            data_dump["password"]
        )
        data_dump.pop("password")
        user = await self.repo.create(data_dump)

        return user


async def get_users_service(
    repo: UserRepository = Depends(get_user_reposetory),
) -> UserService:
    return UserService(repo)
