# Fichier de webscrapping des données du site avec les infos du JO : https://olympics.com/fr/
import urllib.request as urlreq
from bs4 import BeautifulSoup
import json
from scrapping import *

#* Constants
URL_SPORTS = 'https://olympics.com/en/sports/'
OUTPUT_FILE = './output.json'

def insertSports():

    #* Scrapping

    req = urlreq.Request(URL_SPORTS)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36')

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
    cleanSports = cleanData(jsonObject)

    print(len(cleanSports))

    #* Insert data to DB
    insertData("INSERT INTO sport(id, name, url, odf_code, pictogram) VALUES(%s, %s, %s, %s, %s)", dictToSequence(cleanSports))
    
insertSports()