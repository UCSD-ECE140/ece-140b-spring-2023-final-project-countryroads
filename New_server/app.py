# main.py
from fastapi import FastAPI, WebSocket, Request, WebSocketDisconnect
import websockets
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import uvicorn
import mysql.connector as mysql
from dotenv import load_dotenv
import os
import json
from math import radians, sin, cos, sqrt, atan2
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

# Store connected clients and room information
load_dotenv("credentials.env")

db_host = os.environ['MYSQL_HOST']
db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']
db_name = os.environ['MYSQL_DATABASE']

range_km = 1  # Example range in kilometers

@app.get("/")
async def get():
    return HTMLResponse(open("index.html").read())


@app.websocket("/ws/{room}/{client_id}")
async def websocket_endpoint(websocket: WebSocket, room: str, client_id: str):
    await websocket.accept()

    if room not in app.state.connections:
        app.state.connections[room] = []

    app.state.connections[room].append({"client_id": client_id, "websocket": websocket})
    try:
        while True:
            data = await websocket.receive_text()
            await broadcast(data, room, client_id, range_km)
    except WebSocketDisconnect:
        print(f"WebSocket connection closed for client ID: {client_id}")


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            parsed_data = json.loads(data)
            latitude = parsed_data["latitude"]
            longitude = parsed_data["longitude"]
            
            db = mysql.connect(user=db_user, password=db_pass, host=db_host)
            cursor = db.cursor()
            cursor.execute("USE CountryRoads")
            query = "REPLACE INTO Users (client_id, longitude, latitude) VALUES (%s, %s, %s)"
            cursor.execute(query, (client_id, longitude, latitude))
            db.commit()
    except WebSocketDisconnect:
        print(f"WebSocket connection closed for client ID: {client_id}")


async def broadcast(message: str, room: str, sender_id: str, range_km: float):
    print(app.state.connections)

    if room in app.state.connections:
        sender_location = get_user_location(sender_id)
        if sender_location is None:
            print("Sender location not found")
            return

        sender_latitude, sender_longitude = sender_location
        users_in_range = get_users_in_range(sender_latitude, sender_longitude, range_km)
        print("USERS IN RANGE:", users_in_range)

        for connection in app.state.connections[room]:
            # print(connection)
            client_id = connection["client_id"]
            websocket = connection["websocket"]
            if client_id != sender_id and int(client_id) in users_in_range:
                print("SENDING MESSAGE!!!!!- ", message)
                await websocket.send_text(message)

def get_user_location(client_id: str):
    db = mysql.connect(user=db_user, password=db_pass, host=db_host)
    cursor = db.cursor()
    cursor.execute("USE CountryRoads")

    query = "SELECT latitude, longitude FROM Users WHERE client_id = %s"
    cursor.execute(query, (client_id,))
    result = cursor.fetchone()

    if result:
        latitude, longitude = result
        return latitude, longitude

    return None


@app.on_event("startup")
async def startup_event():
    # Connect to the db and create a cursor object
    db = mysql.connect(user=db_user, password=db_pass, host=db_host)
    cursor = db.cursor()

    # Creating and using the database
    cursor.execute("CREATE DATABASE IF NOT EXISTS CountryRoads;")
    cursor.execute("USE CountryRoads;")

    cursor.execute("DROP TABLE IF EXISTS Users;")
    try:
        cursor.execute("""
        CREATE TABLE Users (
            client_id   INTEGER        NOT NULL  AUTO_INCREMENT  PRIMARY KEY,
            longitude   VARCHAR(100)   NOT NULL, 
            latitude    VARCHAR(100)   NOT NULL
        );
        """)
    except RuntimeError as err:
        print("Runtime error: {0}".format(err))
    db.commit()
    app.state.connections = {}

@app.put("/update_location")
async def update_location(request: Request):
    db = mysql.connect(user=db_user, password=db_pass, host=db_host)
    cursor = db.cursor()
    cursor.execute("USE CountryRoads")
    tmp_dict = await request.json()
    query = "REPLACE INTO Users (client_id, longitude, latitude) VALUES (%s, %s, %s)"
    values = [tmp_dict['client_id'], tmp_dict['longitude'], tmp_dict['latitude']]
    cursor.execute(query, values)
    db.commit()
    return {"message": "Location updated successfully"}


@app.delete("/delete_user")
async def delete_user(request: Request):
    db = mysql.connect(user=db_user, password=db_pass, host=db_host)
    cursor = db.cursor()
    cursor.execute("USE CountryRoads")
    tmp_dict = await request.json()
    query = "DELETE FROM Users WHERE client_id = %s"
    values = [tmp_dict['client_id']]
    cursor.execute(query, values)
    db.commit()
    return {"message": "User deleted successfully"}


def get_users_in_range(latitude, longitude, range_km):
    print("LATITUDE: ", latitude)
    print("LONGITUDE: ", longitude)
    print("RANGE_KM: ", range_km)
    db = mysql.connect(user=db_user, password=db_pass, host=db_host)
    cursor = db.cursor()
    cursor.execute("USE CountryRoads")

    # range_meters = 0
    # SQL query to retrieve users within the specified range
    query = """
        SELECT client_id, latitude, longitude
        FROM Users
        WHERE (
            6371 *
            2 *
            ASIN(
                SQRT(
                    POWER(SIN((RADIANS(%s) - RADIANS(latitude)) / 2), 2) +
                    COS(RADIANS(latitude)) *
                    COS(RADIANS(%s)) *
                    POWER(SIN((RADIANS(%s) - RADIANS(longitude)) / 2), 2)
                )
            )
        ) <= %s
    """
    query_data = (latitude, latitude, longitude, range_km)

    try:
        # Execute the query
        cursor.execute(query, query_data)

        # Fetch all the results
        results = cursor.fetchall()

        # Process the results
        users_in_range = []
        for row in results:
            client_id, lat, lon = row
            users_in_range.append(client_id)

        return users_in_range

    except mysql.Error as error:
        print("Error fetching users:", error)
    finally:
        # Close the cursor and connection
        cursor.close()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=6543)
