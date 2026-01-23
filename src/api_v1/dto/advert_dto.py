# файл: dto/advert_dto.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from uuid import UUID  # Добавляем UUID


class AdvertCreateDTO(BaseModel):
    content: str
    description: str
    price: int
    id_category: UUID = Field(None, example="bd29f255-50ab-4967-bc77-475a5fbe7952")# UUID  # Оставляем UUID как в твоей БД
    #category: str = Field(None, example = "Транспорт")

class AdvertUpdateFullDTO(BaseModel):
    content: str = None
    description: str = None
    price: int = None
    id_category: UUID = Field(None, example="bd29f255-50ab-4967-bc77-475a5fbe7952")

class AdvertUpdatePartialDTO(BaseModel):
    content: Optional[str] = None
    description: Optional[str] = None
    price: Optional[int] = None
    id_category: Optional[UUID] = Field(None, example="bd29f255-50ab-4967-bc77-475a5fbe7952")
    #category: Optional[str] = Field(None, example="Транспорт")


class AdvertSearchRequestDTO(BaseModel):
    query: Optional[str] = None
    id_category: Optional[UUID] = None  # Меняем на UUID

class AdvertResponseDTO(BaseModel):
    id: UUID  # Оставляем UUID как в твоей БД
    content: str
    description: str
    price: int
    id_category: UUID  # Оставляем UUID
    id_seller: UUID    # Оставляем UUID
    date_created: datetime
    category_name: Optional[str] = None
    seller_name: Optional[str] = 'some guy'
    is_created: Optional[bool] = None
    is_liked: Optional[bool] = None
    is_bought: Optional[bool] = None
    is_bought_by_current: Optional[bool] = None


class AdvertListResponseDTO(BaseModel):
    items: List[AdvertResponseDTO]
