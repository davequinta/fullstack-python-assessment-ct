from pydantic import BaseModel, Field

class ProductBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    description: str | None = None
    price: float = Field(..., gt=0)
    stock: int = Field(..., ge=0)

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int

    class Config:
        from_attributes = True
