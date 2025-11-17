# from sqlalchemy.orm import relationship

from .base import Base, BaseModelMixin

from .category import Category
from .post import Posts

# Posts.category = relationship("Categories", back_populates="posts")
# Category.posts = relationship("Posts", back_populates="category")


__all__ = ["Base", "BaseModelMixin", "Category", "Posts"]
