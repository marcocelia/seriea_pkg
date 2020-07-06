import matplotlib.pyplot as plt
from seriea_pkg.data.rounds import Rounds
from seriea_pkg.data.team_results import TeamResult

class RoundGraphics:

    def __init__(self, rounds):
        if not isinstance(rounds, Rounds):
            raise TypeError('Rounds object required')
        self.ranking = rounds.ranking()
        self.teams = sorted(list(self.ranking.index.values))


    def compare_by(self, label):
        """
        Display a bar plot comparing all teams belonging to a round with respect to the provided column
        """
        allowed = TeamResult.get_labels()
        if label not in allowed:
            raise ValueError(f'Provided {label} is not valid. Available labels are: ' + ','.join(allowed))

        fig = plt.figure(figsize=(20, 10))
        ax = fig.subplots()
        ax.set_title(f'Team Comparison for {label}')
        ax.bar(self.teams, self.ranking.loc[self.teams,label])
        fig.tight_layout()

