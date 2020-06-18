from seriea_pkg.data.rounds_validator import RoundsValidator
from seriea_pkg.data.team_results import TeamResult
from seriea_pkg.data import constants as consts
from seriea_pkg.data.match_type import MatchType
import pandas as pd

class Rounds:

    def __init__(self, dataframe):
        validator = RoundsValidator()
        if not validator.is_valid(dataframe):
            raise ValueError('Provided dataframe is not valid')
        self.df = dataframe

    def __str__(self):
        return self.df.to_string(index=False)

    def __iter__(self):
        return self.df.iterrows()

    def __len__(self):
        return self.df.shape[0]

    def subset(self, start, end):
        mask = (self.df[consts.ROUND] >= start) & (self.df[consts.ROUND] <= end )
        return Rounds(self.df[mask])

    def ranking(self):
        teams = self.df[consts.HOME_TEAM].unique()
        rank = {}
        for t in teams:
            res = self.compute_team_results(t)
            rank[t] = res.as_tuple()

        labels = TeamResult.get_labels()
        sort = TeamResult.sort_criteria()
        rank_df = pd.DataFrame.from_dict(rank, orient='index', columns=labels).sort_values(sort, ascending=False)
        return rank_df

    def filter_team(self, teamname, strtype=MatchType.TYPE_ALL):
        mtype = MatchType(strtype)

        if mtype.all():
            mask = (self.df[consts.HOME_TEAM] == teamname) | (self.df[consts.AWAY_TEAM] == teamname)
        elif mtype.home():
            mask = (self.df[consts.HOME_TEAM] == teamname)
        else:
            mask = (self.df[consts.AWAY_TEAM] == teamname)

        return Rounds(self.df[mask])

    def compute_team_results(self, teamname, strtype=MatchType.TYPE_ALL):
        mtype = MatchType(strtype)

        if mtype.all():
            return self.compute_team_results(teamname, MatchType.TYPE_HOME) + self.compute_team_results(teamname, MatchType.TYPE_AWAY)

        team_rounds = self.filter_team(teamname, strtype)

        if mtype.home():
            won_mask = (team_rounds.df[consts.GOALS_HOME] > team_rounds.df[consts.GOALS_AWAY])
            scored_mask = consts.GOALS_HOME
            suffered_mask = consts.GOALS_AWAY
        else:
            won_mask = (team_rounds.df[consts.GOALS_AWAY] > team_rounds.df[consts.GOALS_HOME])
            scored_mask = consts.GOALS_AWAY
            suffered_mask = consts.GOALS_HOME

        draw_mask = (team_rounds.df[consts.GOALS_HOME] == team_rounds.df[consts.GOALS_AWAY])

        won = team_rounds.df[won_mask].shape[0]
        draw = team_rounds.df[draw_mask].shape[0]
        loss = team_rounds.df.shape[0] - won - draw
        scored = team_rounds.df[scored_mask].sum()
        suffered = team_rounds.df[suffered_mask].sum()
        return TeamResult(teamname, won, draw, loss, scored, suffered)
