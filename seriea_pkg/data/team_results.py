from seriea_pkg.data import constants as consts
from seriea_pkg.data.match_type import MatchType
from itertools import starmap

class TeamResult:

    def __init__(self, *, team, won, draw, loss, scored, max_scored, conceded, max_conceded):
        self.team = team
        self.won = won
        self.draw = draw
        self.loss = loss
        self.played = won + draw + loss
        self.points = 3*self.won + self.draw
        self.points_avg = self.points/self.played if self.played > 0 else 0
        self.scored = scored if self.played > 0 else 0
        self.max_scored = max_scored if self.played > 0 else 0
        self.conceded = conceded if self.played > 0 else 0
        self.max_conceded = max_conceded if self.played > 0 else 0

    def __add__(self, o):
        if self.team != o.team:
            raise ValueError('Cannot sum result from different teams')

        return TeamResult(
            team =self.team,
            won = self.won + o.won,
            draw = self.draw + o.draw,
            loss = self.loss + o.loss,
            scored = self.scored + o.scored,
            conceded = self.conceded + o.conceded,
            max_scored = max(self.max_scored, o.max_scored),
            max_conceded = max(self.max_conceded, o.max_conceded)
        )

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
