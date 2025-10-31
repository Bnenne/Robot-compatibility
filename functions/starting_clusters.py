import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import DBSCAN
from pandas import DataFrame
import pandas as pd

class StartingClusters:
    def __init__(self):
        self.starting_positions = []
        self.df = DataFrame(columns=['x', 'y'])

        self.clusters = {}

        sns.set_theme(style="ticks")

    def format_data(self):
        for pos in self.starting_positions:
            new_data = DataFrame({'x': [0], 'y': [pos[1]]})
            self.df = pd.concat([self.df, new_data])

    def create_graphs(self):
        fig, ax = plt.subplots(figsize=(7, 3))

        sns.stripplot(
            data=self.df,
            x='y',
            y='label',
            hue='label',
            size=7.5,
            jitter=0.025
        )

        ax.xaxis.grid(True)
        ax.set(ylabel="")
        sns.despine(trim=True, left=True)

        plt.savefig('starting_clusters.png', bbox_inches='tight')
        plt.close(fig)

    def cluster(self):
        eps = 15
        min_samples = 1

        db = DBSCAN(eps=eps, min_samples=min_samples)
        db.fit(self.df)

        label_df = DataFrame({'label': db.labels_})
        self.df = pd.concat([self.df.reset_index(drop=True), label_df.reset_index(drop=True)], axis=1)

        cluster_counts = self.df['label'].value_counts()
        multi_instance_clusters = cluster_counts[cluster_counts > 1].index

        if len(multi_instance_clusters) > 3:
            eps += 1
            self.cluster()
            return

        filtered_df = self.df[self.df['label'].isin(multi_instance_clusters)].copy()
        unique_labels = filtered_df['label'].unique()

        mapping = {unique_labels[i]: f"auto_{i + 1}" for i in range(len(unique_labels))}
        filtered_df['label'] = filtered_df['label'].replace(mapping)

        self.df = filtered_df

    def mass(self):
        auto_labels = self.df['label'].unique().tolist()

        self.clusters = dict.fromkeys(auto_labels, 0)

        for label in auto_labels:
            y_sum = self.df[self.df['label'] == label]['y'].sum()
            count = len(self.df[self.df['label'] == label])

            self.clusters[label] = (y_sum / count) / 337