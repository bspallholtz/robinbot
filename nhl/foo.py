#!/usr/bin/python3.7
import requests
import pickle

game_data = []
year = '2019'
season_type = '02' 
max_game_ID = 1

r = requests.get(url='http://statsapi.web.nhl.com/api/v1/game/')
print(r.text)
#data = r.json()
#print(data)


