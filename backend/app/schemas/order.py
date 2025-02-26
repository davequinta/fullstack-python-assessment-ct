from pydantic import BaseModel
from typing import List

class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int

class OrderCreate(BaseModel):
    customer_name: str
    customer_email: str
    items: List[OrderItemCreate]

class OrderItem(BaseModel):
    product_id: int
    quantity: int

    class Config:
        from_attributes = True

class Order(BaseModel):
    id: int
    status: str  # Include the status field
    items: List[OrderItem]

    class Config:
        from_attributes = True
