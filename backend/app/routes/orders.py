from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.order import Order, OrderItem
from app.models.product import Product
from app.schemas.order import OrderCreate, OrderItemCreate, Order as OrderSchema
from app.database import get_db

router = APIRouter()

@router.post("/orders/", response_model=OrderSchema)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    db_order = Order(
        customer_name=order.customer_name,
        customer_email=order.customer_email,
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    for item in order.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Product {item.product_id} not found")

        db_order_item = OrderItem(
            product_id=item.product_id,
            quantity=item.quantity,
            price=product.price,
            order_id=db_order.id
        )
        db.add(db_order_item)
    
    db.commit()  
    return db_order


@router.get("/orders/", response_model=list[OrderSchema])
def get_orders(db: Session = Depends(get_db)):
    return db.query(Order).all()

@router.get("/orders/{order_id}", response_model=OrderSchema)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.put("/orders/{order_id}/status", response_model=OrderSchema)
def update_order_status(order_id: int, status: str, db: Session = Depends(get_db)):
    """
    Update the status of an existing order.
    """
    # Fetch the order
    order = db.query(Order).filter(Order.id == order_id).first()
    
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    order.status = status
    db.commit() 
    db.refresh(order) 
    return order
