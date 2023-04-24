# Fichier de webscrapping des données du site avec les infos du JO : https://olympics.com/fr/
import urllib.request as urlreq
from bs4 import BeautifulSoup
import json
from scrapping import *

def cleanSportData(data):
    cleanSports = []
    
    for i, sport in enumerate(data):
        cleanSport = {}
        for key in sport:
            if key in SPORTS_SITE_PROPERTIES:
                index = SPORTS_SITE_PROPERTIES.index(key)
                cleanSport[SPORTS_DB_PROPERTIES[index]] = sport[key]
                
        print(f"In loop, n°{i}")
        print(cleanSport)
        cleanSports.append(cleanSport)
    
    return cleanSports

def insertSports():

    #* Scrapping

    req = urlreq.Request(URL_SPORTS)
    req.add_header('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0')

    soup = BeautifulSoup(
        urlreq.urlopen(req), "lxml"
    )

    sportDivs = soup.find(id="all-sports").find('react-component')['data-sport-list']

    jsonObject = json.loads(str(sportDivs))
    print(jsonObject[0])

    #* Saving to a file
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(str(sportDivs))
        
    #* Clean the data to the needed properties
    cleanSports = cleanSportData(jsonObject)
    print(f"{len(cleanSports)} sports retrieved")

    #* Insert data to DB
    insertData("INSERT INTO sport(id, name, url, odf_code, pictogram) VALUES(%s, %s, %s, %s, %s)", dictToSequence(cleanSports))
    
insertSports()