from scrapping import *

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

def getEventsForURL():
    listOfEvents = []

    #Get events from database