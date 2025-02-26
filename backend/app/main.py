from fastapi import FastAPI
from app.routes import product, orders

app = FastAPI()

app.include_router(product.router)
app.include_router(orders.router)

@app.get("/")
def read_root():
    return {"message": "API is running"}
