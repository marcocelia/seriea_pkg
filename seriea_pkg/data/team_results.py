from seriea_pkg.data import constants as consts
from seriea_pkg.data.match_type import MatchType
from itertools import starmap

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
        pairs = list(zip(self.get_labels(), self.as_tuple()))
        return self.team + ': ' + ', '.join(starmap(lambda x,y: f"{x}={y}", pairs))

    def as_tuple(self):
        return (self.points, self.played, self.won, self.draw, self.loss, self.scored, self.suffered)

    @classmethod
    def get_labels(cls):
        return ('Points', 'Played', 'Won', 'Draw', 'Loss', 'Goals Scored', 'Goals Suffered')

    @classmethod
    def sort_criteria(cls):
        return ['Points', 'Goals Scored']
