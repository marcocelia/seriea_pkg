from seriea_pkg.data import constants as consts
from seriea_pkg.data.match_type import MatchType
from itertools import starmap

class TeamResult:

    def __init__(self, team, won, draw, loss, scored, max_scored, conceded,max_conceded):
        self.team = team
        self.won = won
        self.draw = draw
        self.loss = loss
        self.played = won + draw + loss
        self.points = 3*self.won + self.draw
        self.points_avg = self.points/self.played
        self.scored = scored
        self.max_scored = max_scored
        self.conceded = conceded
        self.max_conceded = max_conceded

    def __add__(self, o):
        if self.team != o.team:
            raise ValueError('Cannot sum result from different teams')

        twon = self.won + o.won
        tdraw = self.draw + o.draw
        tloss = self.loss + o.loss
        tscored = self.scored + o.scored
        tconceded = self.conceded + o.conceded
        mmax_scored = max(self.max_scored, o.max_scored)
        mmax_conceded = max(self.max_conceded, o.max_conceded)

        return TeamResult(self.team, twon, tdraw, tloss, tscored, mmax_scored, tconceded, mmax_conceded)

    def __str__(self):
        pairs = list(zip(self.get_labels(), self.as_tuple()))
        return self.team + ': ' + ', '.join(starmap(lambda x,y: f"{x}={y}", pairs))

    def as_tuple(self):
        return (
            self.points,
            self.points_avg,
            self.played,
            self.won,
            self.draw,
            self.loss,
            self.scored,
            self.max_scored,
            self.conceded,
            self.max_conceded
        )

    @classmethod
    def get_labels(cls):
        return ('PS', 'PS-AVG', 'P', 'W', 'D', 'L', 'GS', 'GS-M', 'GC', 'GC-M')

    @classmethod
    def sort_criteria(cls):
        return ['PS', 'GS']
