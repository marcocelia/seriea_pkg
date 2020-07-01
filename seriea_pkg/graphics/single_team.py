import matplotlib.pyplot as plt
from seriea_pkg.data.team_results import TeamResult

class SingleTeamGraphics:

    def __init__(self, teamRes):
        # if teamRes is not TeamResult:
        #     raise TypeError('Required TeamResult object')
        self.teamRes = teamRes


    def roundsGraph(self):
        labels = 'Won', 'Draw', 'Loss'
        sizes = [ self.teamRes.won, self.teamRes.draw, self.teamRes.loss ]
        fig = plt.figure(figsize=(10, 10))
        ax1 = fig.subplots()
        ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, labeldistance=None)
        ax1.legend(title="Results")
        ax1.axis('equal')
        plt.show()

