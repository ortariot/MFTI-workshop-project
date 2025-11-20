from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext
from jose import JWTError, jwt

from repositories.user import UserRepository, get_user_reposetory
from schemas.auth_schema import TokenData
from schemas.user_schema import UserResponse
from configs.app import settings


security = HTTPBearer()


class AuthService:

    def __init__(
        self, repo: UserRepository, credentials: HTTPAuthorizationCredentials | None = None
    ):
        self.repo = repo
        self.pwd_context = CryptContext(schemes=["sha512_crypt"])
        self.credentials = credentials

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    async def authenticate_user(self, email: str, password: str):
        user = await self.repo.get_by_email(email)

        if not user:
            return False
        if not self.verify_password(password, user.hashed_password):
            return False
        return user

    def create_access_token(self, data: dict, expires_delta: timedelta = None):

        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
            
        data.update({"exp": expire})

        encoded_jwt = jwt.encode(
            data,
            settings.auth.sekret_key,
            algorithm=settings.auth.algorithm,
        )
        return encoded_jwt

    async def get_current_user(
        self,
    ):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        try:
            payload = jwt.decode(
                self.credentials.credentials,
                settings.auth.sekret_key,
                algorithms=[settings.auth.algorithm],
            )
            email: str = payload.get("sub")
            if email is None:
                raise credentials_exception
            token_data = TokenData(email=email)
        except JWTError:
            raise credentials_exception

        user = await self.repo.get_by_email(email)
        if user.status is False:
            raise HTTPException(status_code=400, detail="Inactive user")
        if user is None:
            raise credentials_exception
        return user


async def get_req_service(
    repo: UserResponse = Depends(get_user_reposetory),
) -> AuthService:
    return AuthService(repo)


async def get_auth_service(
    repo: UserResponse = Depends(get_user_reposetory),
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> AuthService:
    return AuthService(repo, credentials)
