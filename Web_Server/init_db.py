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
db =mysql.connect(user=db_user, password=db_pass, host=db_host)
cursor = db.cursor()

#creating and using database
cursor.execute("CREATE DATABASE if not exists CountryRoads;")
cursor.execute("USE CountryRoads;")

cursor.execute("drop table if exists Users;")
try:
   cursor.execute("""
   CREATE TABLE Users (
       user       VARCHAR(100) NOT NULL PRIMARY KEY,
       location  VARCHAR(100) NOT NULL
   );
 """)
except RuntimeError as err:
   print("runtime error: {0}".format(err))
db.commit()
