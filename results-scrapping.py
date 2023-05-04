# Fichier de webscrapping pour récupérer tous les résultats sur le site : https://olympics.com/en/olympic-games/

import urllib.request as urlreq
from bs4 import BeautifulSoup
import json
import time
import random
from scrapping import *
from DAO.requests import *

#* Constants
OUTPUT_FILE = './results.json'
LOG_FILE = './logs.txt'
TIME_TO_SLEEP = 0.5

def getResults(edition, event):
    url = f"https://olympics.com/en/olympic-games/{edition[1]}/results/{event[2]}/{event[1]}"

    result = [] # Tableau pour accueillir les résultats de l'URL scrappée

    try:
        req = prepareRequest(url)
        soup = BeautifulSoup(
            urlreq.urlopen(req), "lxml"
        )
        if soup.find('div', {"class": "Tablestyles__Wrapper-sc-xjyvs9-0"}).find_all("div", {"data-cy": "single-athlete-result-row"}) != []:
            resultsDiv = soup.find('div', {"class": "Tablestyles__Wrapper-sc-xjyvs9-0"}).find_all("div", {"data-cy": "single-athlete-result-row"})
            for div in resultsDiv:
                resultData = {}
                resultData["rank"] = div.find("span", {"data-cy": "medal-main"}).text
                resultData["Team"] = div.find("div", {"class": "styles__FlagWithLabelWrapper-sc-rh9yz9-1"}).find("span").text
                resultData["athlete"] = div.find("h3", {"data-cy": "athlete-name"}).text
                try:
                    resultData["result"] = div.find("div", {"class": "styles__ResultInfoWrapper-sc-rh9yz9-2"}).find("span", {"data-cy": "result-info-content"}).text
                except:
                    resultData["result"] = None
                try:
                    resultData["Notes"] = div.find("div", {"class": "styles__NotesInfoWrapper-sc-rh9yz9-3"}).find("span", {"data-cy", "result-info-content"}).text
                except:
                    resultData["Notes"] = None
                resultData["event"] = event[0]
                resultData["edition"] = edition[0]
                result.append(resultData)
        else:
            resultsDiv = soup.find('div', {"class": "Tablestyles__Wrapper-sc-xjyvs9-0"}).find_all("div", {"data-cy": "team-result-row"})
            for i, div in enumerate(resultsDiv):
                resultData = {}
                resultData["rank"] = div.find("span", {"data-cy": "medal-main"}).text
                resultData["Team"] = div.find("div", {"data-cy": "country-name-row-"+str(i+1)}).text
                resultData["athlete"] = None
                try:
                    resultData["result"] = div.find("div", {"class": "styles__ResultInfoWrapper-sc-rh9yz9-2"}).find("span", {"data-cy": "result-info-content"})
                except:
                    resultData["result"] = None
                try:
                    resultData["Notes"] = div.find("div", {"class": "styles__NotesInfoWrapper-sc-rh9yz9-3"}).find("span", {"data-cy", "result-info-content"}).text
                except:
                    resultData["Notes"] = None
                resultData["event"] = event[0]
                resultData["edition"] = edition[0]
                result.append(resultData)
        print(f"Les résultats du {event[1]} > {event[2]} ont été scrappées")
    except:
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"URL inexistante : {url} >>> {current_time}\n")
    finally:
        return result


def run():
    resultsList = [] # Liste pour accueillir toutes les données

    editions = getEditionsForURL()
    events = getEventsForURL()

    for edition in editions:
        for event in events:
            result = getResults(edition, event)
            for data in result:
                if data not in resultsList:
                    resultsList.append(data)
            time.sleep(random.uniform(TIME_TO_SLEEP/2, TIME_TO_SLEEP*1.5))
        # Ecriture d'un log à chaque editions entierement scrappée
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"Les résultats d'une édition ont été scrappé : {edition}   >>>  {current_time}\n")
    # Ecriture des données dans un fichier JSON au cas où l'insertion en base ne passe pas
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
                json.dump(resultsList, f)
    
    insertData("INSERT INTO events_results(rank, team, participant, results, notes, id_event, id_edition) VALUES(%s, %s, %s, %s, %s, %s, %s)", dictToSequence(resultsList))


run()
