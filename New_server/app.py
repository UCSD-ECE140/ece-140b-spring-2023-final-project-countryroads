# main.py
from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import uvicorn
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# Store connected clients and room information
clients = {}
rooms = {}


@app.get("/")
async def get():
    return HTMLResponse(open("index.html").read())


@app.websocket("/ws/{room}/{client_id}")
async def websocket_endpoint(websocket: WebSocket, room: str, client_id: str):
    await websocket.accept()

    if room not in app.state.connections:
        app.state.connections[room] = []

    app.state.connections[room].append({"client_id": client_id, "websocket": websocket})

    while True:
        data = await websocket.receive_text()
        await broadcast(data, room, client_id)


async def broadcast(message: str, room: str, sender_id: str):
    print(app.state.connections)
    
    if room in app.state.connections:
        for connection in app.state.connections[room]:
            client_id = connection["client_id"]
            websocket = connection["websocket"]
            if client_id != sender_id:
                print("SENDING MESSAGE!!!!!- ", message)
                await websocket.send_text(message)


@app.on_event("startup")
async def startup_event():
    app.state.connections = {}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=6543)
