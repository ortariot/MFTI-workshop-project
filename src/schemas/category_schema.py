from uuid import UUID
from typing import Optional

from pydantic import BaseModel, ConfigDict


class CategoryBase(BaseModel):
    name: str
    desc: Optional[str] = None


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    desc: Optional[str] = None


class CategoryResponse(CategoryBase):
    model_config = ConfigDict(from_attributes = True)

    uuid: UUID

    # class Config:
    #     from_attributes = True
