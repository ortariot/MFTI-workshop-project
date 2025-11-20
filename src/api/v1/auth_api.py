from datetime import datetime, timedelta


from fastapi import Depends, HTTPException, status, APIRouter


from services.auth_service import AuthService, get_auth_service, get_req_service
from services.user_service import UserService, get_users_service
from schemas.auth_schema import Token, Login
from schemas.user_schema import UserRegistrate, UserResponse
from configs.app import settings

router = APIRouter()


@router.post("/registrate", response_model=UserResponse)
async def registrate(
    form_data: UserRegistrate,
    service: UserService = Depends(get_users_service),
):
    res = await service.create_user(form_data)

    return res


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Login, service: AuthService = Depends(get_req_service)
):
    user = await service.authenticate_user(form_data.email, form_data.password)
    print(user)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(
        minutes=settings.auth.access_token_expire_minutes
    )
    access_token = service.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me/", response_model=UserResponse)
async def read_users_me(
    service: AuthService = Depends(get_auth_service),
):
    current_user = await service.get_current_user()

    return current_user


@router.get("/protected")
async def protected_route(
    service: AuthService = Depends(get_auth_service),
):
    current_user = await service.get_current_user()

    return {
        "message": f"Hello {current_user.username if current_user.username else current_user.email}, this is a protected route!"
    }
