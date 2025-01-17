from pydantic import BaseModel
from datetime import datetime

class PaymentOut(BaseModel):
    id: int
    stripe_payment_id: str
    amount: int
    currency: str
    timestamp: datetime

    class Config:
        orm_mode = True
