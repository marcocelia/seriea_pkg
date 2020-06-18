import unittest
from seriea_pkg.services.football_api import FootballAPIClient

class ServicesTest(unittest.TestCase):

    def tearDown(self):
        super().tearDown()
        FootballAPIClient.unset_secret_key_path()


    def test_footballapi_client(self):
        fbclient = FootballAPIClient()
        with self.assertRaises(ValueError):
            fbclient.get_league_id(2017)

        FootballAPIClient.set_secret_key_path('keyfile.txt')

        # Registration make working either old or new client
        self.assertEqual(fbclient.get_league_id(2017), 28)
        newclient = FootballAPIClient()
        self.assertEqual(newclient.get_league_id(2017), 28)

