from seriea_pkg.services import football_api as fbapi
from seriea_pkg.data.rounds import Rounds
from os import listdir
from os.path import isfile, join as Path
from seriea_pkg.data import constants
import pandas as pd
import re

def load_dataset(season, dir):
    fname = f"{season}.csv"
    dataset = [f for f in listdir(dir) if isfile(Path(dir, f)) and f == fname]
    if not dataset:
        fixtures = download_dataset(season)
        df = pd.DataFrame.from_dict(fixtures)
        df.to_csv(Path(dir, fname), index=False)
    else:
        df = pd.read_csv(Path(dir, fname))
    return Rounds(df)

def download_dataset(season):
    fat_fixtures = fbapi.get_league_rounds(season)
    fixtures = list(map(reduce_fixture, fat_fixtures))
    return fixtures

def reduce_fixture(src):
    dest = dict()
    m = re.match(r'Regular\sSeason\s*-\s*(\d{1,2})', src['round'])
    dest[constants.ROUND] = int(m.group(1))
    dest[constants.HOME_TEAM] = src['homeTeam']['team_name']
    dest[constants.AWAY_TEAM] = src['awayTeam']['team_name']
    dest[constants.GOALS_HOME] = src['goalsHomeTeam']
    dest[constants.GOALS_AWAY] = src['goalsAwayTeam']
    return dest