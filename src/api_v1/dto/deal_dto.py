from pydantic import BaseModel, Field
from uuid import UUID
from typing import List

class DealCreateRequestDTO(BaseModel):
    advert_id: UUID = Field(..., example="a1b2c3d4-1234-5678-9012-abcdef123456")

class DealResponseDTO(BaseModel):
    id: UUID = Field(..., example="b2c3d4e5-2345-6789-0123-bcdef1234567")
    advert_id: UUID = Field(..., example="a1b2c3d4-1234-5678-9012-abcdef123456")
    customer_id: UUID = Field(..., example="c3d4e5f6-3456-7890-1234-cdef12345678")


class DealListResponseDTO(BaseModel):
    items: List[DealResponseDTO]