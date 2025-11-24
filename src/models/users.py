from typing import Any

from sqlalchemy import Column, String, Boolean

from .base import Base, BaseModelMixin


class User(Base, BaseModelMixin):
    __tablename__ = "users"

    username = Column(String)
    full_name = Column(String)
    email = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    status = Column(Boolean, nullable=False, default=True)
    
    def __repr__(self) -> str:
        return (
            f"uuid - {self.uuid}, username - {self.username}"
            f"full_name - {self.full_name} email - {self.email} "
            f" status - {self.status}"
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "uuid": self.uuid,
            "username": self.username,
            "full_name": self.full_name,
            "email": self.email,
            "status": self.status,
        }
