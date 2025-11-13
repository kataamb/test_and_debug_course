from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from uuid import UUID

class Deal(BaseModel):
    id: UUID
    id_advert: UUID
    id_customer: UUID
    date_created: Optional[datetime] = None
    address: str   = "online"
