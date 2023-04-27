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
# import RPi.GPIO as GPIO

app = FastAPI()

# Mount the static directory
app.mount("/public", StaticFiles(directory="public"), name="public")

#root route
@app.get("/", response_class=HTMLResponse)
def get_html() -> HTMLResponse:
   with open("index.html") as html:
       return HTMLResponse(content=html.read())






if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=6543)


