# файл: dto/advert_dto.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from uuid import UUID  # Добавляем UUID


class AdvertCreateDTO(BaseModel):
    title: str
    description: str
    price: int
    category_id: UUID  # Оставляем UUID как в твоей БД


class AdvertUpdateDTO(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[int] = None
    category_id: Optional[UUID] = None


class AdvertSearchRequestDTO(BaseModel):
    query: Optional[str] = None
    category_id: Optional[UUID] = None  # Меняем на UUID
    min_price: Optional[int] = None
    max_price: Optional[int] = None


class AdvertResponseDTO(BaseModel):
    id: UUID  # Оставляем UUID как в твоей БД
    title: str
    description: str
    price: int
    category_id: UUID  # Оставляем UUID
    seller_id: UUID    # Оставляем UUID
    created_at: datetime
    updated_at: datetime
    category_name: Optional[str] = None
    seller_name: Optional[str] = None
    likes_count: Optional[int] = None
    is_liked: Optional[bool] = None


class AdvertListResponseDTO(BaseModel):
    items: List[AdvertResponseDTO]
