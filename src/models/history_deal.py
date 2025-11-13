from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID

class HistoryDeal(BaseModel):
    id: UUID | None = None
    id_deal: UUID
    id_customer: UUID
    status: int = 1
    date_created: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        from_attributes = True
