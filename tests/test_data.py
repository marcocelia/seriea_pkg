import unittest
from seriea_pkg.data import dataset
from seriea_pkg.data import constants as consts
from seriea_pkg.data.match_type import MatchType
from seriea_pkg.services.football_api import FootballAPIClient

class DataTest(unittest.TestCase):

    def setUp(self):
        super().setUp()
        FootballAPIClient.set_secret_key_path('keyfile.txt')
        self.rounds = dataset.load_dataset(2017, 'datasets')

    def tearDown(self):
        super().tearDown()
        FootballAPIClient.unset_secret_key_path()

    def test_filter_team(self):
        team = 'Juventus'

        team_rounds = self.rounds.filter_team(team)
        self.assertEqual(len(team_rounds), 38)
        for k, row in team_rounds:
            self.assertTrue(row[consts.HOME_TEAM] == team or row[consts.AWAY_TEAM] == team)

        team_home_rounds = self.rounds.filter_team(team, MatchType.TYPE_HOME)
        self.assertEqual(len(team_home_rounds), 19)
        for k, row in team_home_rounds:
            self.assertTrue(row[consts.HOME_TEAM] == team)

        team_away_rounds = self.rounds.filter_team(team, MatchType.TYPE_AWAY)
        self.assertEqual(len(team_away_rounds), 19)
        for k, row in team_away_rounds:
            self.assertTrue(row[consts.AWAY_TEAM] == team)


    def test_teams_fixtures(self):
        int_vs_juv = self.rounds.filter_team('Juventus').compute_team_results('Inter')
        juv_vs_int = self.rounds.filter_team('Inter').compute_team_results('Juventus')

        self.assertEqual(juv_vs_int.won, int_vs_juv.loss)
        self.assertEqual(juv_vs_int.draw, int_vs_juv.draw)
        self.assertEqual(juv_vs_int.loss, int_vs_juv.won)
        self.assertEqual(juv_vs_int.played, int_vs_juv.played)
        self.assertEqual(juv_vs_int.scored, int_vs_juv.suffered)
        self.assertEqual(juv_vs_int.suffered, int_vs_juv.scored)

        # Season 2017 :
        # Juventus - Inter: 0-0
        # Inter - Juventus: 2-3
        self.assertEqual(juv_vs_int.won, 1)
        self.assertEqual(juv_vs_int.draw, 1)
        self.assertEqual(juv_vs_int.loss, 0)
        self.assertEqual(juv_vs_int.scored, 3)
        self.assertEqual(juv_vs_int.suffered, 2)

        juv_vs_int_home = self.rounds.filter_team('Inter').compute_team_results('Juventus', 'home')
        self.assertEqual(juv_vs_int_home.won, 0)
        self.assertEqual(juv_vs_int_home.draw, 1)
        self.assertEqual(juv_vs_int_home.loss, 0)
        self.assertEqual(juv_vs_int_home.scored, 0)
        self.assertEqual(juv_vs_int_home.suffered, 0)

        juv_away_vs_int_home = self.rounds.filter_team('Inter', 'home').compute_team_results('Juventus', 'away')
        int_home_vs_juv_away = self.rounds.filter_team('Juventus', 'away').compute_team_results('Inter', 'home')
        self.assertEqual(juv_away_vs_int_home.won, int_home_vs_juv_away.loss)
        self.assertEqual(juv_away_vs_int_home.draw, int_home_vs_juv_away.draw)
        self.assertEqual(juv_away_vs_int_home.loss, int_home_vs_juv_away.won)
        self.assertEqual(juv_away_vs_int_home.played, int_home_vs_juv_away.played)
        self.assertEqual(juv_away_vs_int_home.scored, int_home_vs_juv_away.suffered)
        self.assertEqual(juv_away_vs_int_home.suffered, int_home_vs_juv_away.scored)

        # It should not be possibile to have a match where both teams play home or away
        juv_home_vs_int_home = self.rounds.filter_team('Juventus', 'home').compute_team_results('Inter', 'home')
        juv_away_vs_int_away = self.rounds.filter_team('Juventus', 'away').compute_team_results('Inter', 'away')
        self.assertEqual(juv_home_vs_int_home.played, 0)
        self.assertEqual(juv_away_vs_int_away.played, 0)

if __name__ == '__main__':
    unittest.main()