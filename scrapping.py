import psycopg2
import os
import urllib.request as urlreq
from bs4 import BeautifulSoup

from commons import *

def dictToSequence(data):
    return [tuple(dict.values()) for dict in data]

def listToSequence(data):
    return [(val,) for val in data]

def dbConfig():
    return {
        'database': 'projet-data-jo',
        'host': os.environ.get('DBJO_HOST') or 'localhost',
        'user': os.environ.get('DBJO_USERNAME') or 'postgres',
        'password': os.environ.get('DBJO_PWD') or 'postgres',
        'port': os.environ.get('DBJO_PORT') or 5432
    }
    
def prepareRequest(URL):
    req = urlreq.Request(URL)
    req.add_header('User-Agent', os.getenv('USER_AGENT'))

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