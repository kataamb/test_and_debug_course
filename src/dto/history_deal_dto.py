from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

class HistoryDealDTO(BaseModel):
    id: UUID
    deal_id: UUID
    advert_id: UUID
    content: str
    description: str
    price: int
    category_name: str
    customer_name: str
    status: int
    address: str
    date_created: datetime

    @property
    def status_text(self):
        return {
            0: "Активна",
            1: "Завершена",
            2: "Отменена"
        }.get(self.status, "Неизвестно")
