from pydantic import BaseModel, Field
from uuid import UUID
from typing import List

class CategoryResponseDTO(BaseModel):
    id: UUID = Field(..., examples=["a1b2c3d4-1234-5678-9012-abcdef123456"])
    name: str = Field(..., examples=["Electronics"])

class CategoryListResponseDTO(BaseModel):
    items: List[CategoryResponseDTO]