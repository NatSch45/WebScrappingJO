# Fichier de webscrapping des données du site avec les infos du JO : https://olympics.com/fr/
import urllib
import urllib.request
from bs4 import BeautifulSoup
import json
from scrapping import *

#* Constants
URL_EDITIONS = 'https://olympics.com/en/olympic-games'
OUTPUT_FILE = './output.json'

def insertEditions():

    #* Scrapping

    soup = BeautifulSoup(
        urllib.request.urlopen(URL_EDITIONS), "lxml"
    )
    # Récupère les données avec les liens pour chaque editions
    editionDivs = soup.find('head').find('script', {"type": "application/ld+json"})
    # print(editionDivs.text)

    jsonObject = json.loads(editionDivs.text)
    # print(jsonObject['itemListElement'][0]['url'])
    # print(len(jsonObject['itemListElement']))

    all_url = []

    for i in range(0, len(jsonObject['itemListElement'])):
        all_url.append(jsonObject['itemListElement'][i]['url'])
    
    print(all_url[0])


#     #* Saving to a file
#     with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
#         f.write(str(editionDivs))
        
#     #* Clean the data to the needed properties
#     cleanEditions = cleanData(jsonObject)

#     print(len(cleanEditions))

#     #* Insert data to DB
#     # insertData("INSERT INTO edition(id, name, url, odf_code, pictogram) VALUES(%s, %s, %s, %s, %s)", dictToSequence(cleanEditions))
    
insertEditions()