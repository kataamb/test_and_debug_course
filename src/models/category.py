from pydantic import BaseModel
from uuid import UUID

class Category(BaseModel):
    id: UUID
    name: str
