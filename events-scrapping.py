# Fichier de webscrapping des données du site avec les infos du JO : https://olympics.com/fr/
import urllib
import urllib.request
from bs4 import BeautifulSoup
import json
import time
import random
from scrapping import *

#* Constants
OUTPUT_FILE = './output.json'
TIME_TO_SLEEP = 0.5

def getEditionsForURL():

    listOfEdtions = []
    # Get data from database

    editions = selectData("SELECT name FROM edition")
    for edition in editions:
        listOfEdtions.append(edition[0].replace(' ', '-').lower())

    return listOfEdtions

def getSportsForURL():
    listOfSports = []
    # Get data from database

    sports = selectData("SELECT name FROM sport")
    for sport in sports:
        listOfSports.append(sport[0].replace(' ', '-').lower())

    return listOfSports


def insertEvents(edition, sport):
    print(edition)

def run():
    edtionsInUrl = getEditionsForURL()
    sportsInUrl = getSportsForURL()
    insertEvents(edtionsInUrl[1], sportsInUrl[0])
    print(len(sportsInUrl))

run()