# Fichier de webscrapping des données du site avec les infos du JO : https://olympics.com/fr/
import urllib
import urllib.request
from bs4 import BeautifulSoup
import psycopg2
import json
import os

#* Constants
URL_SPORTS = 'https://olympics.com/en/sports/'
OUTPUT_FILE = './output.json'

#* Connect to databse

connection = psycopg2.connect(
    database='projet-data-jo',
    host=os.environ.get('DBJO_HOST') or 'localhost',
    user=os.environ.get('DBJO_USERNAME') or 'postgres',
    password=os.environ.get('DBJO_PWD') or 'postgres',
    port=os.environ.get('DBJO_PORT') or 5432
)

cursor = connection.cursor()

cursor.execute("")

connection.close()


#* Scrapping

sportsList = []

soup = BeautifulSoup(
    urllib.request.urlopen(URL_SPORTS), "lxml"
)

sportDivs = soup.find(id="all-sports").find('react-component')['data-sport-list']

jsonObject = json.loads(str(sportDivs))
print(len(jsonObject))

#* Saving to a file

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(str(sportDivs))
