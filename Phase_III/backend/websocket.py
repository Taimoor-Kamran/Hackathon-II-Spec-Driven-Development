from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict, List
import json
from datetime import datetime

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, List[WebSocket]] = {}  # user_id -> list of connections

    async def connect(self, websocket: WebSocket, user_id: int):
        await websocket.accept()
        if user_id not in self.active_connections:
            self.active_connections[user_id] = []
        self.active_connections[user_id].append(websocket)

    def disconnect(self, websocket: WebSocket, user_id: int):
        if user_id in self.active_connections:
            self.active_connections[user_id].remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast_to_user(self, message: str, user_id: int):
        if user_id in self.active_connections:
            for connection in self.active_connections[user_id]:
                try:
                    await connection.send_text(message)
                except WebSocketDisconnect:
                    # Remove disconnected connection
                    self.active_connections[user_id].remove(connection)
                    if not self.active_connections[user_id]:
                        del self.active_connections[user_id]

    async def broadcast_task_update(self, message: dict, user_ids: List[int]):
        """Broadcast task update to multiple users (for collaboration)"""
        for user_id in user_ids:
            if user_id in self.active_connections:
                for connection in self.active_connections[user_id]:
                    try:
                        await connection.send_text(json.dumps(message))
                    except WebSocketDisconnect:
                        # Remove disconnected connection
                        self.active_connections[user_id].remove(connection)
                        if not self.active_connections[user_id]:
                            del self.active_connections[user_id]

manager = ConnectionManager()

# Create a FastAPI sub-application for WebSocket routes
from fastapi import FastAPI
websocket_app = FastAPI()

@websocket_app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    await manager.connect(websocket, user_id)
    try:
        while True:
            # This will keep the connection alive and listen for messages
            # For now, we'll just keep the connection open for broadcasting
            data = await websocket.receive_text()
            # Parse the received data (in a real app, you'd handle different message types)
            try:
                message_data = json.loads(data)
                # Echo the message back to the sender for now
                await manager.send_personal_message(data, websocket)
            except json.JSONDecodeError:
                # If it's not JSON, just echo back as is
                await manager.send_personal_message(f"Received: {data}", websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket, user_id)