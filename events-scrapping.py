# Fichier de webscrapping des données du site avec les infos du JO : https://olympics.com/fr/
import urllib
import urllib.request as urlreq
from bs4 import BeautifulSoup
import json
import time
import random
from scrapping import *

#* Constants
OUTPUT_FILE = './output.json'
TIME_TO_SLEEP = 0.5

# index = 1

def getEditionsForURL():

    listOfEdtions = []
    # Get editions from database

    editions = selectData("SELECT name FROM edition")
    for edition in editions:
        listOfEdtions.append(edition[0].replace(' ', '-').lower())

    return listOfEdtions

def getSportsForURL():
    listOfSports = []
    # Get sports from database

    sports = selectData("SELECT name FROM sport")
    for sport in sports:
        listOfSports.append(sport[0].replace(' ', '-').lower())

    return listOfSports


def getEvents(edition, sport):
    eventURL = f"https://olympics.com/en/olympic-games/{edition}/results/{sport}"

    result = []
    # Scrapping
    try:
        req = urlreq.Request(eventURL)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36')

        soup = BeautifulSoup(
            urlreq.urlopen(req), "lxml"
        )

        eventsDiv = soup.find_all('div', {"class": "styles__RowTitle-sc-282810-1"})

        # Pour chaque évenement, on va chercher son nom en minuscule.
        for div in eventsDiv:
            eventData = {}
            name = div.find("h2").text.lower()
            # global index
            # eventData["id"] = index
            eventData["name"] = name
            eventData["sport"] = f"discipline-{sport}"
            # index += 1
            result.append(eventData)
        return result

    except:
        print("Tentative de scrapping sur une URL inexistante")
    finally:
        return result

def insertEvents(editions):

    #* Saving to a file
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(str(editions))

    # Ajout des index pour chaque event
    for i in range(0, len(editions)):
        editions[i]["id"] = i+1
    print(f"Les index ont été ajoutés pour les {len(editions)} évenements")
    insertData("INSERT INTO event(name, sport, id) VALUES(%s, %s, %s)", dictToSequence(editions))
    print(f"Les données ont été insérées en base.")


def run():
    eventList = []

    edtionsInUrl = getEditionsForURL()
    sportsInUrl = getSportsForURL()
    # Je vais pouvoir boucler sur chaque editions et exécuter la fonction insertEvents dans la boucle
    for i in range(0, len(edtionsInUrl) -1):
        for j in range(0, len(sportsInUrl) -1):
            # eventList.append(data for data in getEvents(edtionsInUrl[i], sportsInUrl[j]))
            events = getEvents(edtionsInUrl[i], sportsInUrl[j])

            if len(events) != 0:
                for data in events:
                    if data not in eventList:
                        eventList.append(data)

            time.sleep(random.uniform(TIME_TO_SLEEP/2, TIME_TO_SLEEP*1.5))

            print(f"{j+1} sport sur {len(sportsInUrl)} scrappé pour cette édition >> {((j+1)/len(sportsInUrl))*100}%")
        print(f"{i+1} éditions sur {len(edtionsInUrl)} scrappé >> {((i+1)/len(edtionsInUrl))*100}%")
    
    insertEvents(eventList)


run()