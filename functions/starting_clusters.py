import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN


class StartingClusters:
    def __init__(self):
        self.starting_positions = []

        self.array_x = []
        self.array_y = []

        self.labels = []

    def arrayify_data(self):
        for pos in self.starting_positions:
            self.array_x.append(0)
            self.array_y.append(pos[1])

    def create_graphs(self):
        plt.scatter(x=self.array_x, y=self.array_y, labels=self.labels)
        plt.xlim(-1, 1)
        plt.ylim(0, 337)

        plt.show()

    def cluster(self):
        eps = 20
        min_samples = 1

        db = DBSCAN(eps=eps, min_samples=min_samples)
        db.fit(self.array_y)

        self.labels = db.labels_