# Fichier de webscrapping des données du site avec les infos du JO : https://olympics.com/fr/
import json
import time
import random

from scrapping import *

def getCountryIdFromName(allCountries, countryName):
    for country in allCountries:
        if countryName == country[1]:
            return country[0]
    print(f"WARN: The country {countryName} has not been found in the list of all countries.")
    return ""

def getEditionIdFromName(allEditions, editionName):
    for edition in allEditions:
        if editionName == edition[1]:
            return edition[0]
    print(f"WARN: The edition {editionName} has not been found in the list of all editions.")
    return ""

def insertMedals():

    #* Scrapping
    
    req = prepareRequest(URL_EDITIONS)
    
    soup = BeautifulSoup(
        urlreq.urlopen(req), "lxml"
    )
    # Récupère les données avec les liens pour chaque editions
    editionDivs = soup.find('head').find('script', {"type": "application/ld+json"})
    
    jsonObject = json.loads(editionDivs.text)
    # print(jsonObject['itemListElement'][0]['url'])
    # print(len(jsonObject['itemListElement']))

    allUrl = []
    allCountries = selectData("SELECT * FROM country")
    allEditions = getAllEditions()
    allMedals = []


    for i in range(0, len(jsonObject['itemListElement'])):
        allUrl.append(jsonObject['itemListElement'][i]['url'].replace(".com/", ".com/en/"))

    # Iterate over all editions URL
    for i, url in enumerate(allUrl[4:]): # Remove all editions that have not yet taken place (from athens-1896 to beijing-2022)
        urlArr = url.split('/')
        edition = urlArr[len(urlArr)-1]
    
        req = prepareRequest(f"{url}/medals")
        
        editionSoup = BeautifulSoup(
            urlreq.urlopen(req), "lxml"
        )
    
        tableContent = editionSoup.find(id="__next").find("div", {"data-cy": "table-content"})
        if not tableContent: # If tableContent is not found, skip the country scrapping part
            continue
        
        countries = [x.text for x in tableContent.find_all("span", {"data-cy": "country-name"})]
        medals = list(map(lambda l: l.replace('-', '0'), [x.text for x in tableContent.find_all("span", {"data-cy": "medal-main"})]))
        
        for j, country in enumerate(countries):
            editionId = getEditionIdFromName(allEditions, edition)
            countryId = getCountryIdFromName(allCountries, country)
            golds = medals[j*4]
            silvers = medals[j*4+1]
            bronzes = medals[j*4+2]
            if editionId != "" and countryId != "":
                allMedals.append((editionId, countryId, golds, silvers, bronzes))
        
        print(f"Nbr of countries of the {edition} edition : {len(countries)}")
        time.sleep(TIME_DELAY + random.randint(0, 10)/10)
    
    #* Insert data to DB
    insertData("INSERT INTO medals(id_edition, id_country, gold_medals, silver_medals, bronze_medals) VALUES(%s, %s, %s, %s, %s)", allMedals)
    print(f"{len(allMedals)} new lines in table public.medals")
    
insertMedals()