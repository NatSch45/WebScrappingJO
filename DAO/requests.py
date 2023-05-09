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
    REPLACEMENT_CHARS = [(' - ', '-'), (' -', '-'), (' + ', '-plus-'), (' +', '-over-'), (' ', '-'), ('.', '-'), ('\'s', ''), ('\'', ''), ('(', ''), (')', ''), ('(w+m)', 'women-and-men'), (':', '-'), (',', '-')]

    #Get events from database
    events = selectData("SELECT * FROM event")
    for event in events:
        formattedEvent = event[1].lower()
        for chars in REPLACEMENT_CHARS:
            formattedEvent.replace(chars[0], chars[1])
            
        listOfEvents.append((event[0], formattedEvent, event[2].replace('discipline-', '')))

    return listOfEvents
