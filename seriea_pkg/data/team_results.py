from seriea_pkg.data import constants as consts
from seriea_pkg.data import dataset
from seriea_pkg.data.match_type import MatchType
from itertools import starmap
import csv

class TeamResult:
    """
    A wrapper class for the most common team results and statistics
    """

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
        """
        Convert self to a tuple
        """
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
        """
        Returns the following labels:
        - Points
        - Points Average
        - Played
        - Won
        - Draw
        - Loss
        - Goals scored
        - Max goals scored in a single round
        - Goals conceeded
        - Max goals conceeded in a single round
        """
        return ('PS', 'PS-AVG', 'P', 'W', 'D', 'L', 'GS', 'GS-M', 'GC', 'GC-M')

    @classmethod
    def sort_criteria(cls):
        """
        Return an array containing the columns with respect to TeamResults shall be ordered
        """
        return ['PS', 'GS']

    def to_csv(self, fname, *args):
        dir = args[0] if args else dataset.get_default_stats_path()
        f = open(f'{dir}/{fname}.csv', 'w')
        with f:
            writer = csv.writer(f)
            writer.writerows([self.__class__.get_labels(), self.as_tuple()])