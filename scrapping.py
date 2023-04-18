import psycopg2
import os

SPORTS_SITE_PROPERTIES = ['id', 'name', 'url', 'odfCode', 'pictogram']
SPORTS_DB_PROPERTIES = ['id', 'name', 'url', 'odf_code', 'pictogram']

def cleanData(data):
    cleanSports = []
    
    for i, sport in enumerate(data):
        cleanSport = {}
        for key in sport:
            if key in SPORTS_SITE_PROPERTIES:
                index = SPORTS_SITE_PROPERTIES.index(key)
                cleanSport[SPORTS_DB_PROPERTIES[index]] = sport[key]
                
        # print("In loop, n°" + str(i))
        # print(cleanSport)
        cleanSports.append(cleanSport)
    
    
    return cleanSports

def dictToSequence(data):
    return [tuple(dict.values()) for dict in data]
        

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