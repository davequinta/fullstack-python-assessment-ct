from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse
from app.database import get_db

router = APIRouter(prefix="/products", tags=["products"])

#Create Product
@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    """
    Create a new product in the database.
    
    - Returns: The created product.
    - Raises:
        - 400: Database integrity error.
        - 500: Unexpected error.
    """
    new_product = Product(**product.model_dump())
    db.add(new_product)
    
    try:
        db.commit()
        db.refresh(new_product)
        return new_product
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Database integrity error: Duplicate or invalid entry.")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Unexpected error: {str(e)}")

#Get All Products
@router.get("/", response_model=list[ProductResponse])
def get_products(db: Session = Depends(get_db)):
    """
    Retrieve all products from the database.
    """
    return db.query(Product).all()

#Get a Single Product
@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific product by its ID.

    - Returns: The product details.
    - Raises:
        - 404: If the product is not found.
    """
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product

#Update a Product
@router.put("/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, product_data: ProductUpdate, db: Session = Depends(get_db)):
    """
    Update an existing product.

    - Returns: The updated product.
    - Raises:
        - 404: If the product does not exist.
        - 500: If an unexpected database error occurs.
    """
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    for key, value in product_data.model_dump().items():
        setattr(product, key, value)

    try:
        db.commit()
        db.refresh(product)
        return product
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Unexpected error: {str(e)}")

#Delete a Product
@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    """
    Delete a product by its ID.

    - Returns: No content.
    - Raises:
        - 404: If the product does not exist.
    """
    deleted = db.query(Product).filter(Product.id == product_id).delete()  #More efficient deletion
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    db.commit()
    return 
