from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime, timezone
from pydantic import ConfigDict


class Advert(BaseModel):
    id: UUID | None = None
    content: str
    description: str
    id_category: UUID
    price: int
    id_seller: UUID
    date_created: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    model_config = ConfigDict(arbitrary_types_allowed=True)