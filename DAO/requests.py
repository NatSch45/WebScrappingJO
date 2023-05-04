from scrapping import *

def getEditionsForURL():

    listOfEdtions = []
    # Get editions from database

    editions = selectData("SELECT id, name FROM edition")
    for edition in editions:
        listOfEdtions.append((edition[0], edition[1].replace(' ', '-').replace('.', '').replace('\'', '-').lower()))

    return listOfEdtions

def getSportsForURL():
    listOfSports = []
    # Get sports from database

    sports = selectData("SELECT name FROM sport")
    for sport in sports:
        listOfSports.append(sport[0].replace(' ', '-').replace('.', '').replace('\'', '-').lower())

    return listOfSports

def getEventsForURL():
    listOfEvents = []

    #Get events from database
    events = selectData("SELECT * FROM event")
    for event in events:
        listOfEvents.append((event[0], event[1].replace(' - ', '-').replace(' -', '-').replace(' + ', '-plus-').replace(' +', '-over-').replace(' ', '-').replace('.', '-').replace('\'s', '').replace('\'', '').replace('(', '').replace(')', '').replace('(w+m)', 'women-and-men').replace(':', '-').replace(',', '-').lower(), event[2].replace('discipline-', '')))

    return listOfEvents
