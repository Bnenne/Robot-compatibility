import matplotlib.pyplot as plt

class StartingClusters:
    def __init__(self):
        self.starting_positions = []

        self.array_x = []
        self.array_y = []

    def arrayify_data(self):
        for pos in self.starting_positions:
            self.array_x.append(0)
            self.array_y.append(pos[1])

    def create_graphs(self):
        plt.scatter(x=self.array_x, y=self.array_y)
        plt.xlim(-1, 1)
        plt.ylim(0, 337)

        plt.show()