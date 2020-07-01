import matplotlib.pyplot as plt
from seriea_pkg.data.team_results import TeamResult

class SingleTeamGraphics:

    def __init__(self, teamRes):
        # if teamRes is not TeamResult:
        #     raise TypeError('Required TeamResult object')
        self.teamRes = teamRes


    def roundsGraph(self):
        # Pie chart, where the slices will be ordered and plotted counter-clockwise:
        labels = 'Win', 'Draw', 'Loss'

        sizes = [
            100*self.teamRes.won/self.teamRes.played,
            100*self.teamRes.draw/self.teamRes.played,
            100*self.teamRes.loss/self.teamRes.played
        ]

        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
                shadow=True, startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.show()

