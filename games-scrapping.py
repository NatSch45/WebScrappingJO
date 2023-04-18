# Fichier pour aller chercher les infos des jeux olympiques d'été

import urllib
import urllib.request
from bs4 import BeautifulSoup

url_games = 'https://olympics.com/en/olympic-games'
games_list = []

soup = BeautifulSoup(urllib.request.urlopen(url_games), "lxml")
head = soup.find('head')
scripts = head.find_all('script')

# for game in games:
#     print("Find a game")
#     edition = game.find("p")
#     games_list.append(edition)

print(scripts)