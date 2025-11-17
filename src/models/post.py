import uuid
from typing import Any

from sqlalchemy import Column, String, Text, ForeignKey
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .base import Base, BaseModelMixin


class Posts(Base, BaseModelMixin):
    __tablename__ = "posts"

    media_id = Column(UUID(as_uuid=True), nullable=False, default=uuid.uuid4)
    desc = Column(Text)

    category_id = Column(
        UUID(as_uuid=True),
        ForeignKey("category.uuid", ondelete="SET NULL"),
        nullable=True,
    )

    # category = relationship("Category", back_populates="posts")
    # category = relationship("Category", backref="posts")
    category = relationship("Category", lazy="joined")

    def __repr__(self) -> str:
        return f""

    def to_dict(self) -> dict[str, Any]:
        return {}
