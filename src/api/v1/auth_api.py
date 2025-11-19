from datetime import datetime, timedelta


from fastapi import Depends, HTTPException, status, APIRouter

from services.auth_service import get_current_active_user, create_access_token, authenticate_user
from schemas.auth_schema import User, Token
from configs.app import settings
from repositories.auth import fake_users_db

router = APIRouter()


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: dict):
    user = authenticate_user(
        fake_users_db, form_data["username"], form_data["password"]
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.auth.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
 

@router.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@router.get("/protected")
async def protected_route(
    current_user: User = Depends(get_current_active_user),
):
    return {
        "message": f"Hello {current_user.username}, this is a protected route!"
    }
