import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime
from sqlalchemy.orm import DeclarativeBase, declarative_mixin
from sqlalchemy.dialects.postgresql import UUID


class Base(DeclarativeBase):
    pass


@declarative_mixin
class BaseModelMixin:
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    create_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    update_at = Column(
        DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )
