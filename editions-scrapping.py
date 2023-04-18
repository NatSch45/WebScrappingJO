# Fichier de webscrapping des données du site avec les infos du JO : https://olympics.com/fr/
import urllib
import urllib.request
from bs4 import BeautifulSoup
import json
from scrapping import *

#* Constants
URL_SPORTS = 'https://olympics.com/en/sports/'
OUTPUT_FILE = './output.json'

def insertEditions():

    #* Scrapping

    soup = BeautifulSoup(
        urllib.request.urlopen(URL_SPORTS), "lxml"
    )

    editionDivs = soup.find(id="all-sports").find('react-component')['data-olympic-editions']

    jsonObject = json.loads(str(editionDivs))
    print(jsonObject[0])

    #* Saving to a file
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(str(editionDivs))
        
    #* Clean the data to the needed properties
    cleanEditions = cleanData(jsonObject)

    print(len(cleanEditions))

    #* Insert data to DB
    # insertData("INSERT INTO edition(id, name, url, odf_code, pictogram) VALUES(%s, %s, %s, %s, %s)", dictToSequence(cleanEditions))
    
insertEditions()