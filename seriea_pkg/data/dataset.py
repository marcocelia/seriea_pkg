from seriea_pkg.services.football_api import FootballAPIClient
from seriea_pkg.data.rounds import Rounds
from os import listdir
from os.path import isfile, dirname, abspath, exists, join as Path
from seriea_pkg.data import constants
import configparser
import pandas as pd
import re

def load_dataset(season, *args):
    if args:
        dir = args[0]
    else:
        dir = get_default_datasets_path()

    fname = f"{season}.csv"
    dataset = [f for f in listdir(dir) if isfile(Path(dir, f)) and f == fname]
    if not dataset:
        fixtures = download_dataset(season)
        df = pd.DataFrame.from_dict(fixtures)
        df.to_csv(Path(dir, fname), index=False)
    else:
        df = pd.read_csv(Path(dir, fname))
    return Rounds(df)

def set_default_datasets_path(dirpath):
    fabsp = abspath(dirpath)
    if not exists(fabsp):
        raise FileNotFoundError(fabsp)

    ini_path = f"{dirname(abspath(__file__))}/config.ini"
    cfg = configparser.ConfigParser()
    cfg.read(ini_path)
    cfg['Datasets']['path'] = fabsp

    with open(ini_path, 'w') as configfile:
        cfg.write(configfile)

def get_default_datasets_path():
    ini_path = f"{dirname(abspath(__file__))}/config.ini"
    cfg = configparser.ConfigParser()
    cfg.read(ini_path)
    if not cfg['Datasets']['path']:
        raise FileNotFoundError('No default dataset dir provided')

    return cfg['Datasets']['path']

def download_dataset(season):
    client = FootballAPIClient()
    fat_fixtures = client.get_league_rounds(season)
    fixtures = list(map(reduce_fixture, filter(lambda it: it['statusShort'] == 'FT', fat_fixtures)))
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