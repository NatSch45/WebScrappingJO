import os
import psycopg2

from scrapping import *

def dbConfig():
    return {
        'database': 'projet-data-jo',
        'host': os.environ.get('DBJO_HOST') or 'localhost',
        'user': os.environ.get('DBJO_USERNAME') or 'postgres',
        'password': os.environ.get('DBJO_PWD') or 'postgres',
        'port': os.environ.get('DBJO_PORT') or 5432
    }

def insertData(query, data):
    conn = None
    try:
        # Read db configuration
        params = dbConfig()
        # Connect to the PostgreSQL db
        conn = psycopg2.connect(**params)
        # Create a new cursor
        cur = conn.cursor()
        # Execute multiple INSERT statement
        cur.executemany(query, data)
        # Commit the changes to the db
        conn.commit()
        # Close communication with the db
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def selectData(query):
    conn = None
    try:
        # Read db configuration
        params =  dbConfig()
        # Connect to the PostgreSQL db
        conn = psycopg2.connect(**params)
        # Create a new cursor
        cur = conn.cursor()
        # Execute the select statement
        cur.execute(query)
        # Fetch the result
        result = cur.fetchall()
        # Close communication with the db
        cur.close()
        # Return the result
        return result
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def getEditionsForURL():

    listOfEdtions = []
    # Get editions from database

    editions = selectData("SELECT name FROM edition")
    for edition in editions:
        listOfEdtions.append(edition[0].replace(' ', '-').lower())

    return listOfEdtions

def getAllEditions():
    # Get all editions from database
    editions = selectData("SELECT id, name FROM edition")

    return [(edition[0], edition[1].replace(' ', '-').replace('.', '').replace('\'', '-').lower()) for edition in editions]

def getSportsForURL():
    listOfSports = []
    # Get sports from database

    sports = selectData("SELECT name FROM sport")
    for sport in sports:
        listOfSports.append(sport[0].replace(' ', '-').lower())

    return listOfSports

def getEventsForURL():
    listOfEvents = []

    #Get events from database