import os
from dotenv import load_dotenv

load_dotenv()

USER_AGENT = os.getenv("USER_AGENT")

SPORTS_SITE_PROPERTIES = ['id', 'name', 'url', 'odfCode', 'pictogram']
SPORTS_DB_PROPERTIES = ['id', 'name', 'url', 'odf_code', 'pictogram']

URL_SPORTS = 'https://olympics.com/en/sports/'
URL_EDITIONS = 'https://olympics.com/en/olympic-games'

OUTPUT_FILE = './output.json'
RESULTS_OUTPUT_FILE = './results.json'
LOG_FILE = './logs.txt'

TIME_DELAY = 1 # second(s)
TIME_TO_SLEEP = 0.5 # second(s)
