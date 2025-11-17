from fastapi import APIRouter, Depends, HTTPException, status

from src.repositories.category import CategoryRepository, get_category_reposetory
from src.schemas.category_schema import CategoryCreate

router = APIRouter()


@router.post("/")
async def create_category(
    category_date: CategoryCreate,
    # reposiory: CategoryRepository = Depends(get_category_reposetory)
    service: CategoryService = Depends(get_service)
):
    if reposiory.get_by_name(category_date.name):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Уже существует"
        )
    
    category = reposiory.create(category_date.model_dump())
    return category





