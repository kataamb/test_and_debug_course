from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID


class UserRegister(BaseModel):
    username: str = Field(..., example="john_doe")
    email: str = Field(..., example="john@example.com")

    full_name: str = Field(...,  example="John Doe")
    phone: Optional[str] = Field(None, example="+1234567890")
    password: str = Field(..., example="123")
    rep_password: str = Field(..., example="123")


class UserLogin(BaseModel):
    email: str = Field(..., example="edward23@yahoo.com")
    password: str = Field(..., example="123")


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
