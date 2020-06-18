from seriea_pkg.data import dataset as data
from seriea_pkg.data.team_results import TeamResult
from seriea_pkg.services.football_api import FootballAPIClient

try:
    fbclient = FootballAPIClient()
    fbclient.get_league_id(2017)
except ValueError as e:
    pass
finally:
    FootballAPIClient.set_secret_key_path('keyfile.txt')
    otherclient = FootballAPIClient()
    otherclient.get_league_id(2017)

# rounds = data.load_dataset(2017, 'datasets')

# r = rounds.ranking()
# print(r)

# t = rounds.compute_team_results('Napoli')
# print(t)

# tinter = rounds.filter_team('Juventus', 'home').compute_team_results('Inter')
# print(tinter)
