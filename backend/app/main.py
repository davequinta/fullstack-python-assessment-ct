from fastapi import FastAPI
from app.routes import product

app = FastAPI()

app.include_router(product.router)

@app.get("/")
def read_root():
    return {"message": "API is running"}
