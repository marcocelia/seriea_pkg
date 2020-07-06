import matplotlib.pyplot as plt
from seriea_pkg.data.team_results import TeamResult

class SingleTeamGraphics:

    def __init__(self, teamRes):
        if not isinstance(teamRes,TeamResult):
            raise TypeError('TeamResult object required')
        self.teamRes = teamRes


    def rounds_graph(self):
        """
        Display a pie plot showing the round's result
        """
        labels = 'Won', 'Draw', 'Loss'
        sizes = [ self.teamRes.won, self.teamRes.draw, self.teamRes.loss ]
        fig = plt.figure(figsize=(10, 10))
        ax = fig.subplots()
        ax.set_title(f'{self.teamRes.team} rounds')
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, labeldistance=None)
        ax.legend(title="Results")
        ax.axis('equal')
        fig.tight_layout()
