import json
from fastapi import WebSocket, WebSocketDisconnect
from fastapi.routing import APIRouter

websocket_router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active: dict[str, WebSocket] = {}

    async def connect(self, ws: WebSocket, user_id: str):
        await ws.accept()
        self.active[user_id] = ws

    def disconnect(self, user_id: str):
        self.active.pop(user_id, None)

    async def broadcast(self, message: dict):
        for ws in self.active.values():
            await ws.send_json(message)

manager = ConnectionManager()

@websocket_router.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    user_id = f"user_{id(ws)}"
    await manager.connect(ws, user_id)
    try:
        while True:
            data = await ws.receive_text()
            payload = json.loads(data)
            await manager.broadcast({"sender": user_id, "data": payload})
    except WebSocketDisconnect:
        manager.disconnect(user_id)
