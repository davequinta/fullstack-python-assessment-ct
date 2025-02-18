from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

router = APIRouter()

@router.websocket("/ws/orders")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for real-time order updates.
    This endpoint will send updates to clients about order status.
    """
    await websocket.accept()  # Accept incoming WebSocket connection
    try:
        while True:
            # Simulating an order status update for the frontend (mock data for now)
            await websocket.send_text("Order status: Your order is in processing!")
    except WebSocketDisconnect:
        print("Client disconnected")
