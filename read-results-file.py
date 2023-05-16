# Python program to read
# json file
import json

from scrapping import dictToSequence, insertData
  
# Opening JSON file
f = open('results_try3.json')

# Returns JSON object as a dictionary
data = json.load(f)
print(f"{len(data)} rows to insert in DB")
insertData(
    "INSERT INTO events_results(rank, team, athlete, results, notes, id_event, id_edition) VALUES(%s, %s, %s, %s, %s, %s, %s)",
    dictToSequence(data)
)

# Closing file
f.close()