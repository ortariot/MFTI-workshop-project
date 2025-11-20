
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$6$rounds=656000$HfkzpTNVPM03g5dS$aXP/kSGL3eaqBVhDuZE6q4466zYNh9g5hQ6wEAVYDUCkvQUrhsOpsLYQfkg/59WSWNOM08xtVZTgHHHPXobPd1",  # "secret"
        "disabled": False,
    }
}

from typing import Any, Optional

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.users import User
from database import get_session


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, user_date: dict) -> User:
        user = User(**user_date)
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def get_by_id(self, id: Any) -> Optional[User]:
        result = await self.db.execute(select(User).where(User.uuid == id))

        return result.scalar_one_or_none()

    async def get_by_name(self, name: str) -> Optional[User]:
        result = await self.db.execute(
            select(User).where(User.username == name)
        )

        return result.scalar_one_or_none()
    
    async def get_by_email(self, email: str) -> Optional[User]:
        result = await self.db.execute(
            select(User).where(User.email == email)
        )

        return result.scalar_one_or_none()

async def get_user_reposetory(
    db: AsyncSession = Depends(get_session),
) -> UserRepository:
    return UserRepository(db)
