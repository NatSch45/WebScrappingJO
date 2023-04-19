# Fichier de webscrapping des données du site avec les infos du JO : https://olympics.com/fr/
import urllib
import urllib.request
from bs4 import BeautifulSoup
import json
import time
import random
from scrapping import *

#* Constants
URL_EDITIONS = 'https://olympics.com/en/olympic-games'
OUTPUT_FILE = './output.json'
TIME_TO_SLEEP = 0.5

def insertEditions():

    #* Scrapping

    soup = BeautifulSoup(
        urllib.request.urlopen(URL_EDITIONS), "lxml"
    )
    # Récupère les données avec les liens pour chaque editions
    editionDivs = soup.find('head').find('script', {"type": "application/ld+json"})

    jsonObject = json.loads(editionDivs.text)
    all_url = []

    # Recuperation de tous les liens des editions pour ensuite boucler dessus pour ouvoir choper chaque informations
    for i in range(0, len(jsonObject['itemListElement'])):
        all_url.append(jsonObject['itemListElement'][i]['url'].replace(".com/", ".com/en/"))
    del all_url[0:4]

    cleanEditions = []

    for url in all_url:
        # Initialisation du dictionnaire pour les données
        cleanEdition = {}
        # Récupération de la soupe de l'url précis
        editionSoup = BeautifulSoup(
            urllib.request.urlopen(url), "lxml"
        )
        # Création d'une liste avec tous les composants html contenant les données à récupérer
        editionData = editionSoup.find(id="__next").find("section", {"class": "styles__Facts-sc-1w4me2-0 gcTVvL"}).contents
        # Ajout d'un index
        cleanEdition[0] = all_url.index(url)
        # Boucle sur chaque élement html sauf le dernier qu'on ne veut pas
        for i in range(0, len(editionData) -1):
            # La 1ère donnée est dans un <h1> donc on prends que le text
            if i == 0:
                cleanEdition[i+1] = editionData[i].text

            # Pour les autres données, elles sont dans des <div> avec un <span> avec du texte qui nous intéresse pas puis le texte de la div.
            # On récupère que la valeur texte de la div avec la boucle (dernier élement dcp)
            else:
                for data in editionData[i].contents:
                    cleanEdition[i+1] = data

        # Ajout de mon dictionnaire de données à la liste qui doit contenir tous les dictionnaires
        cleanEditions.append(cleanEdition)

        print(f"Les données de {url} ont été récupérées >> {(all_url.index(url) / len(all_url))*100}%")
        
        # sleep d'une druée aléatoire pour ne pas attaquer toutes les URL d'un coup
        time.sleep(random.uniform(TIME_TO_SLEEP/2, TIME_TO_SLEEP*1.5))

    #* Saving to a file
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(str(editionDivs))

    #* Insert data to DB
    insertData("INSERT INTO edition(id, name, date, country, athletes, teams, events) VALUES(%s, %s, %s, %s, %s, %s, %s)", dictToSequence(cleanEditions))
    print(f"Les données ont été insérées en base >> {len(cleanEditions)} lignes")
    
insertEditions()