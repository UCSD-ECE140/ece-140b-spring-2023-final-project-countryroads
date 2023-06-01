# main.py
from fastapi import FastAPI, WebSocket, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import uvicorn
import mysql.connector as mysql
from dotenv import load_dotenv
import os
from math import radians, sin, cos, sqrt, atan2

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# Store connected clients and room information
load_dotenv("credentials.env")

db_host = os.environ['MYSQL_HOST']
db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']
db_name = os.environ['MYSQL_DATABASE']

# Example usage
latitude = 40.7128  # Example latitude
longitude = -74.0060  # Example longitude
range_km = 40000  # Example range in kilometers

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

# route to update user's location
@app.put("/update_location")
async def get_json(request: Request):
    print("CALLING UPDATE LOCATION")
    db =mysql.connect(user=db_user, password=db_pass, host=db_host)
    cursor = db.cursor()
    cursor.execute("USE CountryRoads")
    tmp_dict = await request.json()
    print(tmp_dict)
    query = "REPLACE into Users (client_id, longitude, latitude) values (%s, %s, %s)"
    values = [tmp_dict['client_id'], tmp_dict['longitude'], tmp_dict['latitude']]
    cursor.execute(query, values)
    db.commit()
    return 

# route to update user's location
@app.delete("/delete_user")
async def get_json(request: Request):
    users_in_range = get_users_in_range(latitude, longitude, range_km)
    print("USERS In RANGE: ", users_in_range)
    print("CALLING DELETE USER")
    db =mysql.connect(user=db_user, password=db_pass, host=db_host)
    cursor = db.cursor()
    cursor.execute("USE CountryRoads")
    tmp_dict = await request.json()
    print("TMP DICT: ", tmp_dict)
    query = "DELETE FROM Users WHERE client_id = %s"
    values = [tmp_dict['client_id']]
    print("val: ", values)
    cursor.execute(query, values)
    db.commit()
    return 

def get_users_in_range(latitude, longitude, range_km):
    db =mysql.connect(user=db_user, password=db_pass, host=db_host)
    cursor = db.cursor()
    cursor.execute("USE CountryRoads")

    # Convert range_km to meters for consistency
    range_meters = range_km * 1000

    # SQL query to retrieve users within the specified range
    query = """
        SELECT client_id, latitude, longitude
        FROM Users
        HAVING (
            6371 * 2 * 
            ASIN(
                SQRT(
                    POWER(SIN(RADIANS(%s - latitude) / 2), 2) +
                    COS(RADIANS(latitude)) *
                    COS(RADIANS(%s)) *
                    POWER(SIN(RADIANS(%s - longitude) / 2), 2)
                )
            )
        ) <= %s
    """
    query_data = (latitude, latitude, longitude, range_meters)

    try:
        # Execute the query
        cursor.execute(query, query_data)

        # Fetch all the results
        results = cursor.fetchall()

        # Process the results
        users_in_range = []
        for row in results:
            client_id, lat, lon = row
            users_in_range.append({
                "client_id": client_id,
                "latitude": lat,
                "longitude": lon
            })

        return users_in_range

    except mysql.Error as error:
        print("Error fetching users:", error)
    finally:
        # Close the cursor and connection
        cursor.close()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=6543)
