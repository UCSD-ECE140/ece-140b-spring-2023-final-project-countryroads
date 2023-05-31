from fastapi import FastAPI, Request, Form, WebSocket
from fastapi.responses import Response
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles   # Used for serving static files
import uvicorn
from fastapi.responses import RedirectResponse
import os
import bcrypt
import dbutils as db  
from datetime import datetime
from multiprocessing import Process

from urllib.request import urlopen  
import json
import mysql.connector as mysql
from dotenv import load_dotenv
import asyncio
import time

app = FastAPI()

load_dotenv("credentials.env")

db_host = os.environ['MYSQL_HOST']
db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']
db_name = os.environ['MYSQL_DATABASE']

# Mount the static directory
app.mount("/public", StaticFiles(directory="public"), name="public")

#count number of users
user_number = 0

# Store WebSocket connections of connected clients
connected_clients = set()

#root route
@app.get("/", response_class=HTMLResponse)
def get_html() -> HTMLResponse:
   with open("index.html") as html:
       return HTMLResponse(content=html.read())
   
# route to get 
@app.post("/update_location")
async def get_json(request: Request):
    global user_number
    db =mysql.connect(user=db_user, password=db_pass, host=db_host)
    cursor = db.cursor()
    cursor.execute("USE CountryRoads")
    tmp_dict = await request.json()
    tmp_dict["user_num"] = user_number
    print(tmp_dict)

    query = "REPLACE into Users (user, longitude, latitude) values (%s, %s, %s)"
    values = [tmp_dict['user_num'], tmp_dict['longitude'], tmp_dict['latitude']]
    cursor.execute(query, values)
    db.commit()
    return 

# route to get 
@app.post("/new_user")
async def get_json(request: Request):
    global user_number
    user_number += 1
    return 

# Store WebSocket connections of connected clients
connected_clients = set()

# WebSocket endpoint to receive and broadcast audio data
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    # Add the WebSocket connection to the set of connected clients
    connected_clients.add(websocket)

    try:
        while True:
            # Receive audio data from the client
            data = await websocket.receive_text()

            # Log the received audio data
            print(f"Received audio data: {data}")

            # Broadcast the audio data to all other connected clients
            for client in connected_clients:
                if client != websocket:
                    await client.send_text(data)
    finally:
        # Remove the WebSocket connection when the client disconnects
        connected_clients.remove(websocket)
 
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=6543)


