from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import product, orders

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Adjust this to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(product.router)
app.include_router(orders.router)

@app.get("/")
def read_root():
    return {"message": "API is running"}
