# Full-Stack Python Assessment (FastAPI, SQLAlchemy, React, PostgreSQL)

## 🚀 Overview
This project implements a **Full-Stack E-Commerce system** with:
- **Backend**: FastAPI + PostgreSQL + SQLAlchemy
- **Frontend**: Next.js 15 (with TypeScript) + Tailwind CSS
- **Real-time updates**: WebSockets for order status updates
- **Database**: PostgreSQL 15

## Backend Setup (FastAPI + PostgreSQL)

### 1. Install dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Change DATABASE_URL in backend/app/database.py
```python
DATABASE_URL = "postgresql://user:password@localhost/dbname"
```

### 3. Run Migrations
```bash
cd backend
alembic upgrade head
```
### 4. Run FastAPI server
```bash
cd backend
uvicorn app.main:app --reload
```

## Frontend Setup (Next.js 15 + Tailwind CSS)

### 1. Install dependencies
```bash
cd frontend
npm install
```

### 2. Run Next.js server
```bash
cd frontend
npm run dev
```

## Usage
### Backend

The FastAPI backend provides the following endpoints:

- Create an Order (POST /orders/): This endpoint allows customers to create an order by providing their details and the items in their order. The order is saved with a status of processing.
- Update Order Status (PUT /orders/{order_id}/status): This endpoint allows updating the order's status (e.g., from processing to shipped).
= Get All Orders (GET /orders/): Retrieve all orders in the system.
- Get Order by ID (GET /orders/{order_id}): Retrieve a specific order by its ID.
- Real-Time Updates via WebSockets (ws://localhost:8000/ws/orders/{order_id}): This WebSocket endpoint allows clients to listen for real-time updates about the order's status.

You can access the FastAPI Swagger UI at http://localhost:8000/docs to interact with the API.


### Frontend
- The frontend is a React application built with Next.js and Tailwind CSS that listens for real-time updates using WebSockets.
