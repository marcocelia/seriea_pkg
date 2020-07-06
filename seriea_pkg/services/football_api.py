import requests
import json
import configparser
from os.path import abspath, dirname, exists

class FootballAPIClient:
    """
    A simple REST client for Football API
    """

    CFG_INI_PATH = f"{dirname(abspath(__file__))}/config.ini"
    cfg = configparser.ConfigParser()
    cfg.read(CFG_INI_PATH)
    leagues_ep = '{}/leagues/type/league/{}/{}'
    league_ep = '{}/fixtures/league/{}'

    def __init__(self):
        self.headers = {}
        api_cfg = self.__class__.cfg['FootballAPI']
        self.host_v = f'{api_cfg["protocol"]}://{api_cfg["host"]}/{api_cfg["version"]}'
        if api_cfg['secret_key_path']:
            with open(api_cfg['secret_key_path'], 'r') as keyfile:
                self.headers['X-RapidAPI-Key'] = keyfile.read()

    @classmethod
    def set_secret_key_path(cls, filepath):
        """
        Store the path to the file containing the secret key needed to query Football API
        """
        fabsp = abspath(filepath)
        if not exists(fabsp):
            raise FileNotFoundError(fabsp)

        cls.cfg['FootballAPI']['secret_key_path'] = fabsp

        with open(cls.CFG_INI_PATH, 'w') as configfile:
            cls.cfg.write(configfile)

    @classmethod
    def unset_secret_key_path(cls):
        """
        Unregister the current key file path
        """
        cls.cfg['FootballAPI']['secret_key_path'] = ''

        with open(cls.CFG_INI_PATH, 'w') as configfile:
            cls.cfg.write(configfile)

    def get_league_rounds(self, season):
        """
        Given the season year retrieves all rounds belonging to such season
        """
        self.ensure_key_registered()
        l_id = self.get_league_id(season)
        response = requests.get(self.__class__.league_ep.format(self.host_v, l_id), headers=self.headers)
        ret = response.json()
        if ret['api']['results'] == 0:
            return []
        return ret['api']['fixtures']

    def get_league_id(self, season):
        """
        Given the season year returns the Serie A league_id as returned from footbal API
        """
        leagues = self.get_leagues_per_season(season)
        serie_a_id = [x['league_id'] for x in leagues if x['name'] == 'Serie A']
        return serie_a_id[0]

    def get_leagues_per_season(self, season):
        """
        Given the season year list all leagues available for that year
        """
        self.ensure_key_registered()
        raw = requests.get(self.__class__.leagues_ep.format(self.host_v, 'italy', season), headers=self.headers)
        res = raw.json()
        if res['api']['results'] == 0:
            return []
        return res['api']['leagues']

    def ensure_key_registered(self):
        """
        Ensure the secret key is present before making a request to Football API
        """
        if not 'X-RapidAPI-Key' in self.headers:
            if not self.__class__.cfg['FootballAPI']['secret_key_path']:
                raise ValueError('Football API secret key not provided')
            else:
                path = self.__class__.cfg['FootballAPI']['secret_key_path']
                with open(path, 'r') as keyfile:
                    self.headers['X-RapidAPI-Key'] = keyfile.read()
