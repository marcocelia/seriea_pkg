import requests
import json
from os.path import abspath, dirname

cfg = f"{dirname(abspath(__file__))}/conf.json"
with open(cfg) as json_data:
    headers = json.load(json_data)

host_v = 'https://api-football-v1.p.rapidapi.com/v2'
leagues_endpoint = '{}/leagues/type/league/{}/{}'
league_endpoint = '{}/fixtures/league/{}'

def get_league_rounds(season):
    l_id = get_league_id(season)
    response = requests.get(league_endpoint.format(host_v, l_id), headers=headers)
    ret = response.json()
    if ret['api']['results'] == 0:
        return []
    return ret['api']['fixtures']

def get_league_id(season):
    leagues = get_leagues_per_season(season)
    serie_a_id = [x['league_id'] for x in leagues if x['name'] == 'Serie A']
    return serie_a_id[0]

def get_leagues_per_season(season):
    raw = requests.get(leagues_endpoint.format(host_v, 'italy', season), headers=headers)
    res = raw.json()
    if res['api']['results'] == 0:
        return []
    return res['api']['leagues']