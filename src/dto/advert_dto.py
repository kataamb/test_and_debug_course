from datetime import datetime
from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class AdvertWithCategoryDTO(BaseModel):
    id: UUID
    content: str
    description: str
    id_category: UUID
    category_name: str | None = None
    price: int
    id_seller: UUID
    seller_name: str | None = None
    date_created: Optional[datetime]


    is_favorite: bool = False
    is_bought: bool = False
    is_really_bought: bool = False
    is_created: bool = False

    date_deal_created: datetime  | None = None
    date_liked_added: datetime | None = None