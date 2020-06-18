from seriea_pkg.data import constants as consts
from seriea_pkg.data.match_type import MatchType

class TeamResult:

    def __init__(self, team, won, draw, loss, scored, suffered):
        self.team = team
        self.won = won
        self.draw = draw
        self.loss = loss
        self.played = won + draw + loss
        self.points = 3*self.won + self.draw
        self.scored = scored
        self.suffered = suffered

    def __add__(self, o):
        if self.team != o.team:
            raise ValueError('Cannot sum result from different teams')

        twon = self.won + o.won
        tdraw = self.draw + o.draw
        tloss = self.loss + o.loss
        tscored = self.scored + o.scored
        tsuffered = self.suffered + o.suffered

        return TeamResult(self.team, twon, tdraw, tloss, tscored, tsuffered)

    def __str__(self):
        return ', '.join(map(
            lambda x: str(x),
            (self.team, self.points, self.won, self.draw, self.loss, self.scored, self.suffered)
        ))

    @classmethod
    def compute_team_results(cls, rounds, teamname, strtype=MatchType.TYPE_ALL):
        mtype = MatchType(strtype)

        if mtype.all():
            home = rounds.filter_team(teamname, MatchType.TYPE_HOME)
            away = rounds.filter_team(teamname, MatchType.TYPE_AWAY)
            return cls.compute_team_results(home, teamname, MatchType.TYPE_HOME) + cls.compute_team_results(away, teamname, MatchType.TYPE_AWAY)

        if mtype.home():
            won_mask = (rounds.df[consts.GOALS_HOME] > rounds.df[consts.GOALS_AWAY])
            scored_mask = consts.GOALS_HOME
            suffered_mask = consts.GOALS_AWAY
        else:
            won_mask = (rounds.df[consts.GOALS_AWAY] > rounds.df[consts.GOALS_HOME])
            scored_mask = consts.GOALS_AWAY
            suffered_mask = consts.GOALS_HOME

        draw_mask = (rounds.df[consts.GOALS_HOME] == rounds.df[consts.GOALS_AWAY])

        won = rounds.df[won_mask].shape[0]
        draw = rounds.df[draw_mask].shape[0]
        loss = rounds.df.shape[0] - won - draw
        scored = rounds.df[scored_mask].sum()
        suffered = rounds.df[suffered_mask].sum()
        return TeamResult(teamname, won, draw, loss, scored, suffered)
