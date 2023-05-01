from fastapi import FastAPI, Request, Form
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

#root route
@app.get("/", response_class=HTMLResponse)
def get_html() -> HTMLResponse:
   with open("index.html") as html:
       return HTMLResponse(content=html.read())
   
# route to get 
@app.post("/new_user")
async def get_json(request: Request):

    db =mysql.connect(user=db_user, password=db_pass, host=db_host)
    cursor = db.cursor()
    cursor.execute("USE TechAssignment6")
    tmp_dict = await request.json()
    user_number = 0
    tmp_dict["user_num"] = user_number
    print(tmp_dict)

    # query = "insert into Menu_Items (name, price) values (%s, %s)"
    # values = []
    # values.append(tuple(tmp_dict.values()))
    # cursor.executemany(query, values)
    # db.commit()
    return 

if __name__ == "__main__":
    print("here")
    uvicorn.run(app, host="0.0.0.0", port=6543)


