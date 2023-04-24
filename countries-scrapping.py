# Fichier de webscrapping des données du site avec les infos du JO : https://olympics.com/fr/
import urllib
import urllib.request
from bs4 import BeautifulSoup
import json
import time
import random

from scrapping import *

def insertCountries():

    #* Scrapping

    soup = BeautifulSoup(
        urllib.request.urlopen(URL_EDITIONS), "lxml"
    )
    # Récupère les données avec les liens pour chaque editions
    editionDivs = soup.find('head').find('script', {"type": "application/ld+json"})

    jsonObject = json.loads(editionDivs.text)
    # print(jsonObject['itemListElement'][0]['url'])
    # print(len(jsonObject['itemListElement']))

    allUrl = []
    allCountries = []

    for i in range(0, len(jsonObject['itemListElement'])):
        allUrl.append(jsonObject['itemListElement'][i]['url'].replace(".com/", ".com/en/"))
        
    for i in range(10):
        print(f"Iteration n°{i}, DELAY: {TIME_DELAY + random.randint(0, 10)/10}")
        # time.sleep(TIME_DELAY + random.randint(0, 10)/10)
    
    print(allUrl)
    
    for i, url in enumerate(allUrl[4:]): # Remove all editions that have not yet taken place (from athens-1896 to beijing-2022)
        editionSoup = BeautifulSoup(
            urllib.request.urlopen(f"{url}/medals"), "lxml"
        )
    
        tableContent = editionSoup.find(id="__next").find("div", {"data-cy": "table-content"})
        if not tableContent:
            continue
        
        countries = [x.text for x in tableContent.find_all("span", {"data-cy": "country-name"})]
        if i == 0:
            allCountries = countries
        else:
            for country in countries:
                if country not in allCountries:
                    allCountries.append(country)
        
        print(f"Nbr of countries of the {url} edition : {len(countries)}")
        print(f"Total nbr of countries : {len(allCountries)}")
        time.sleep(TIME_DELAY + random.randint(0, 10)/10)
        
    print(allCountries)

    #* Saving to a file
    # with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    #     f.write(str(editionDivs))
        
    #* Clean the data to the needed properties
    # cleanEditions = cleanData(jsonObject)
    # print(len(cleanEditions))

    #* Insert data to DB
    insertData("INSERT INTO country(name) VALUES(%s)", listToSequence(allCountries))
    
insertCountries()