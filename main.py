from seriea_pkg.data import dataset as data
from seriea_pkg.data.team_results import TeamResult
from seriea_pkg.services.football_api import FootballAPIClient

FootballAPIClient.set_secret_key_path('keyfile.txt')
otherclient = FootballAPIClient()
# data.set_default_datasets_path('datasets')
season = data.load_dataset(2019)

print(season.ranking())
# print(season.compute_team_results('Atalanta'))

# print(TeamResult.compute('Atalanta', season))

