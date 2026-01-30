from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID


class UserRegister(BaseModel):
    username: str = Field(default=..., examples=["john_doe"])
    email: str = Field(examples=["john@example.com"])

    full_name: str = Field( examples=["John Doe"])
    phone: Optional[str] = Field(None, examples=["+1234567890"])
    password: str = Field(examples=["123"])
    rep_password: str = Field(examples=["123"])


class UserLogin(BaseModel):
    email: str = Field(examples=["edward23@yahoo.com"])
    password: str = Field(examples=["123"])


class UserResponse(BaseModel):
    id: UUID
    username: str
    email: str
    full_name: str
    phone: Optional[str] = None


    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: Optional[int] = None


class SuccessResponse(BaseModel):
    success: bool = True
    message: str
