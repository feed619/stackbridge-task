from typing import Optional
from pydantic import BaseModel, EmailStr, Field, field_validator


class UserBase(BaseModel):
    email: EmailStr
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    middle_name: Optional[str] = Field(None, max_length=50)


class UserResponse(UserBase):
    is_active: bool


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)
    password_confirm: str

    @field_validator("email")
    def validate_email(cls, v):
        return v.lower().strip() if v else v

    @field_validator("password_confirm")
    def validate_password_confirm(v: str, info) -> str:
        password = info.data.get("password")
        if v != password:
            raise ValueError("Пароли не совпадают")
        return v


class UserUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1, max_length=50)
    last_name: Optional[str] = Field(None, min_length=1, max_length=50)
    middle_name: Optional[str] = Field(None, max_length=50)
    email: Optional[EmailStr] = None
