# backend/app/models/order.py
from sqlalchemy import Column, Integer,Float, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, index=True)
    status = Column(String, default="processing")  # Default status is "processing"
    customer_name = Column(String, index=True)
    customer_email = Column(String)

    # Relationship to OrderItem (One to Many)
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

class OrderItem(Base):
    __tablename__ = 'order_items'

    id = Column(Integer, primary_key=True, index=True)
    quantity = Column(Integer)
    price = Column(Float)
    product_id = Column(Integer, ForeignKey("products.id"))
    order_id = Column(Integer, ForeignKey("orders.id"))

    # Relationship to Product and Order
    product = relationship("Product", back_populates="order_items")
    order = relationship("Order", back_populates="items")