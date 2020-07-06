from seriea_pkg.services.football_api import FootballAPIClient
from seriea_pkg.data.rounds import Rounds
from os import listdir
from os.path import isfile, dirname, abspath, exists, join as Path
from seriea_pkg.data import constants
import configparser
import pandas as pd
import re

def load_dataset(season, *args):
    """
    Retrieve a specific season dataset either from user's archive or form web.
    It is mandatory to specify, at least once, a default dataset directory. Indeed,
    such is used as source for already downloaded datasets or as destination when
    a new dataset is retrieved from thw web.

    Params:
    - season: The season's starting year, e.g. 2019 for season 2019/2020
    - *args (optional): The datasets path. In case it is not provided the function attempts
        to retrieve it from an internal config file and eventually returns an error whether
        it is not found
    """
    dir = args[0] if args else get_default_datasets_path()
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
    """
    Setup the default datasets path that will be used for any subsequent dataset storage or
    retrieval. The path is stored into a package internal config file.

    Params:
    - dirpath: the dasetpath
    """
    fabsp = abspath(dirpath)
    if not exists(fabsp):
        raise FileNotFoundError(fabsp)

    set_config_key('Datasets','path', fabsp)

def set_default_stats_path(dirpath):
    """
    Setup the default datasets path that will be used for any subsequent stats storage or
    retrieval. The path is stored into a package internal config file.

    Params:
    - dirpath: the dasetpath
    """
    fabsp = abspath(dirpath)
    if not exists(fabsp):
        raise FileNotFoundError(fabsp)

    set_config_key('StatsStorage','path', fabsp)

def set_config_key(topic, key, value):
    """
    Writes a generic property under the topic sections in confing.ini file
    Params:
    - topic: The config section
    - key: The property key
    - value: The property value
    """
    ini_path = f"{dirname(abspath(__file__))}/config.ini"
    cfg = configparser.ConfigParser()
    cfg.read(ini_path)
    cfg[topic][key] = value

    with open(ini_path, 'w') as configfile:
        cfg.write(configfile)

def get_default_datasets_path():
    """
    Return the default dataset path from internal config file. Raises a FileNotFoundError
    in case no default dataset have been specified.
    """
    return get_config_key('Datasets','path')

def get_default_stats_path():
    """
    Return the default stats path from internal config file. Raises a FileNotFoundError
    in case no default stats have been specified.
    """
    return get_config_key('StatsStorage','path')

def get_config_key(topic, key):
    """
    Return a generic property belonging to the provided topic from config file
    Params:
    - topic: The config section
    - key: The property key
    """
    ini_path = f"{dirname(abspath(__file__))}/config.ini"
    cfg = configparser.ConfigParser()
    cfg.read(ini_path)
    if not cfg[topic][key]:
        raise FileNotFoundError(f'No default {topic} dir provided')

    return cfg[topic][key]

def download_dataset(season):
    """
    Get all season's available rounds from football web api. Not yet played rounds
    are filtered out, and just a small set of api response's fields is selected.
    """
    client = FootballAPIClient()
    fat_fixtures = client.get_league_rounds(season)
    fixtures = list(map(reduce_fixture, filter(lambda it: it['statusShort'] == 'FT', fat_fixtures)))
    return fixtures

def reduce_fixture(src):
    """
    Given a round fields set, return the subset of field needed for this package
    """
    dest = dict()
    m = re.match(r'Regular\sSeason\s*-\s*(\d{1,2})', src['round'])
    dest[constants.ROUND] = int(m.group(1))
    dest[constants.HOME_TEAM] = src['homeTeam']['team_name']
    dest[constants.AWAY_TEAM] = src['awayTeam']['team_name']
    dest[constants.GOALS_HOME] = src['goalsHomeTeam']
    dest[constants.GOALS_AWAY] = src['goalsAwayTeam']
    return dest