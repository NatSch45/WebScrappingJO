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
TIME_TO_SLEEP = 1

index = 1

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

        eventsDiv = soup.find_all('div', {"class": "styles__RowTitle-sc-282810-1 dvJTpe"})

        

        # Pour chaque évenement, on va chercher son nom en minuscule.
        for div in eventsDiv:
            name = div.find("h2").text.lower()
            global index
            eventData = {"id": index, "name": name, "sport": sport}
            index += 1
            result.append(eventData)

    except:
        print("Tentative de scrapping sur une URL inexistante")
    finally:
        return result


def run():
    eventList = []

    edtionsInUrl = getEditionsForURL()
    sportsInUrl = getSportsForURL()
    # Je vais pouvoir boucler sur chaque editions et exécuter la fonction insertEvents dans la boucle
    for i in range(0, len(edtionsInUrl) -1):
        for j in range(0, len(sportsInUrl) -1):
            eventList.append(data for data in getEvents(edtionsInUrl[i], sportsInUrl[j]))
            time.sleep(random.uniform(TIME_TO_SLEEP/2, TIME_TO_SLEEP*1.5))
        print(eventList)
run()