from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.openapi.models import Response
from pydantic import BaseModel
from fastapi.responses import JSONResponse

app = FastAPI()

# Model for WebSocket message
class WebSocketMessage(BaseModel):
    message: str

# Store active WebSocket connections
active_connections: list[WebSocket] = []

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Broadcast received data to all connected WebSockets
            for connection in active_connections:
                if connection != websocket:
                    await connection.send_text(f"Message: {data}")
    except WebSocketDisconnect:
        active_connections.remove(websocket)
        await websocket.close()

@app.get("/")
async def get():
    return {"message": "WebSocket server running"}

# Swagger documentation for WebSocket messages
@app.post("/send_message/")
async def send_message(message: WebSocketMessage):
    # Example POST endpoint to simulate message sending
    return JSONResponse(content={"message": f"Sent message: {message.message}"})
