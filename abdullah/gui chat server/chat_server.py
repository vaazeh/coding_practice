import asyncio
import websockets
from datetime import datetime

clients = {}  # Map websocket -> username
log_file = open(f"chatroom_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt", "w")

async def handler(websocket):
    try:
        # First message from client will be the username
        username = await websocket.recv()
        clients[websocket] = username
        print(f"{username} connected")
        
        # Broadcast join message
        join_msg = f"*** {username} has joined the chat ***"
        await broadcast(join_msg, websocket)

        async for message in websocket:
            full_msg = f"{username}: {message}"
            await broadcast(full_msg, websocket)
            log_file.write(full_msg + "\n")
            log_file.flush()

    except websockets.ConnectionClosed:
        pass
    finally:
        username = clients.get(websocket, "Unknown")
        leave_msg = f"*** {username} has left the chat ***"
        await broadcast(leave_msg, websocket)
        clients.pop(websocket, None)

async def broadcast(message, sender=None):
    for client in clients.keys():
        if client != sender:
            await client.send(message)

async def main():
    async with websockets.serve(handler, "0.0.0.0", 8760):
        print("Server running on ws://<your-ip>:8760")
        await asyncio.Future()

asyncio.run(main())
