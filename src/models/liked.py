from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from uuid import UUID

class Liked(BaseModel):
    id: UUID
    id_customer: UUID
    id_advert: UUID
    date_created: Optional[datetime] = None