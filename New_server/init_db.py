# Add the necessary imports
import mysql.connector as mysql
import os
import datetime

from dotenv import load_dotenv

load_dotenv("credentials.env")
# Read Database connection variables
db_host = os.environ['MYSQL_HOST']
db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']


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
