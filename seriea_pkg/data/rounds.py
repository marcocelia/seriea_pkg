from seriea_pkg.data.rounds_validator import RoundsValidator
from seriea_pkg.data.team_results import TeamResult
from seriea_pkg.data import constants as consts
from seriea_pkg.data.match_type import MatchType

class Rounds:

    def __init__(self, dataframe):
        validator = RoundsValidator()
        if not validator.is_valid(dataframe):
            raise ValueError('Provided dataframe is not valid')
        self.df = dataframe

    def __str__(self):
        return self.df.to_string(index=False)

    def subset(self, start, end):
        mask = (self.df[consts.ROUND] >= start) & (self.df[consts.ROUND] <= end )
        return Rounds(self.df[mask])

    def filter_team(self, teamname, strtype=MatchType.TYPE_ALL):
        mtype = MatchType(strtype)

        if mtype.all():
            mask = (self.df[consts.HOME_TEAM] == teamname) | (self.df[consts.AWAY_TEAM] == teamname)
        elif mtype.home():
            mask = (self.df[consts.HOME_TEAM] == teamname)
        else:
            mask = (self.df[consts.AWAY_TEAM] == teamname)

        return Rounds(self.df[mask])

    def ranking(self):
        teams = self.df[consts.HOME_TEAM].unique()
        rank = {}
        for t in teams:
            res = TeamResult.compute_team_results(self.filter_team(t), t)
            print(res)

        return rank
