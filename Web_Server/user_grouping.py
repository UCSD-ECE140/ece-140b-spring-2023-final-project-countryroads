import os
import mysql.connector as mysql
from dotenv import load_dotenv

load_dotenv("credentials.env")

db_host = os.environ['MYSQL_HOST']
db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']
db_name = os.environ['MYSQL_DATABASE']


#****************************************************#
#     CALCULATE USER DISTANCE BETWEEN ONE ANOTHER    #
#****************************************************#

#Imports necessary for distance calculation
from math import radians, cos, sin, asin, sqrt

#A negative latitude value means Southern hemisphere
#A negative longitude value means Western hemisphere
#1 degree ~= 111 kilometer distance
def haversine(long1: float, lat1: float, long2: float, lat2: float):
   """
   Calculate the great circle distance in kilometers between two points on the earth (specified in decimal degrees)

   :param float long1: Longitude of first user
   :param float lat1: Latitude of first user
   :param float long2: Longitude of second user
   :param float lat2: Latitude of second user
   :return: distance between two users (in km)
   :rtype: float
   """
   #Convert decimal degrees to radians 
   long1, lat1, long2, lat2 = map(radians, [long1, lat1, long2, lat2])

   #Haversine formula 
   distance_long = long2 - long1 
   distance_lat = lat2 - lat1 
   a = sin(distance_lat/2)**2 + cos(lat1) * cos(lat2) * sin(distance_long/2)**2
   c = 2 * asin(sqrt(a)) 
   r = 6371 # Radius of earth in kilometers. Use 3956 for miles. Determines return value units.
   return c * r


#Connect to the database
def distance_calculation():
   """
   Returns the calculated distance (using haversine function) between two users (in km)
   """
   db = mysql.connect(user=db_user, password=db_pass, host=db_host)
   cursor = db.cursor()
   cursor.execute("USE CountryRoads")

   #Query the database to get the user, longitude, latitude from the Users table to calculate distances
   query = "SELECT user, longitude, latitude FROM Users"
   cursor.execute(query)

   #Find the distance between the users
   for (user, longitude, latitude) in cursor:
      distance = haversine(float(longitude), float(latitude), -118.29, 32.5)
      #print("The distance between user", user, "and the dummy numbers is:", distance)
      return distance



#****************************************************#
#   THROW USERS INTO A GROUP BASED ON RANDOM VALUES  #
#****************************************************#

import random
def insert_dummy():
   """
   Insert dummy testing values into the Users table
   """
   db = mysql.connect(user=db_user, password=db_pass, host=db_host)
   cursor = db.cursor()
   cursor.execute("USE CountryRoads")

   query = "INSERT INTO Users (longitude, latitude) VALUES (%s, %s)"
   values = [(str(random.uniform(115, 119)), str(random.uniform(30.5, 34.5))),
             (str(random.uniform(115, 119)), str(random.uniform(30.5, 34.5))),
             (str(random.uniform(115, 119)), str(random.uniform(30.5, 34.5))),
             (str(random.uniform(115, 119)), str(random.uniform(30.5, 34.5))),
             (str(random.uniform(115, 119)), str(random.uniform(30.5, 34.5))),
             (str(random.uniform(115, 119)), str(random.uniform(30.5, 34.5))),
             (str(random.uniform(115, 119)), str(random.uniform(30.5, 34.5))),
             (str(random.uniform(115, 119)), str(random.uniform(30.5, 34.5))),
             (str(random.uniform(115, 119)), str(random.uniform(30.5, 34.5))),
             (str(random.uniform(115, 119)), str(random.uniform(30.5, 34.5))),
             (str(random.uniform(115, 119)), str(random.uniform(30.5, 34.5)))]
   cursor.executemany(query, values)
   db.commit()
   return


def user_grouping(radius: int):
   """
   Group the users into groups based on a kilometer radius
   
   :param int radius: the radius (in km) that determines user connection range
   :return: None
   """
   insert_dummy()
   pass


def delete_dummy():
   """
   Dump the dummy values that were inserted into Users
   """
   db = mysql.connect(user=db_user, password=db_pass, host=db_host)
   cursor = db.cursor()
   cursor.execute("USE CountryRoads")

   query = "DELETE FROM Users WHERE user>0"
   values = []
   cursor.executemany(query, values)
   db.commit()
   return

insert_dummy()