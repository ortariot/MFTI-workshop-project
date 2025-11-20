import re

from pydantic import BaseModel, field_validator, EmailStr, ConfigDict



class UserBase(BaseModel):
    email: EmailStr


class UserResponse(UserBase):
    status: bool
    full_name: str | None = None
    username: str | None  = None

    model_config = ConfigDict(
        from_attributes=True
    )


class UserRegistrate(UserBase):
    password: str





    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        errors = []
        
        if len(v) < 8:
            errors.append('не менее 8 символов')
        
        if re.search(r'[^A-Za-z0-9!@#$%^&*()_+\-=\[\]{};\':"\\|,.<>/?]', v):
            errors.append('только латинские буквы, цифры и специальные символы')
        
        if not re.search(r'[A-Z]', v):
            errors.append('хотя бы одну заглавную латинскую букву')
        
        if not re.search(r'[a-z]', v):
            errors.append('хотя бы одну строчную латинскую букву')
        
        if not re.search(r'\d', v):
            errors.append('хотя бы одну цифру')
        
        if not re.search(r'[!@#$%^&*()_+\-=\[\]{};\':"\\|,.<>/?]', v):
            errors.append('хотя бы один специальный символ')
        
        if errors:
            raise ValueError(f'Пароль должен содержать: {", ".join(errors)}')
        
        return v


class UserInDB(UserResponse):
    hashed_password: str