import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import DBSCAN
from pandas import DataFrame, Series
import pandas as pd
import numpy as np

class StartingClusters:
    def __init__(self):
        self.starting_positions = []

        self.df = DataFrame(columns=['x', 'y'])
        self.zeros = None

        sns.set_theme(style="ticks")

    def format_data(self):
        for pos in self.starting_positions:
            new_data = DataFrame({'x': [0], 'y': [pos[1]]})
            self.df = pd.concat([self.df, new_data])

        print(self.df.head())

    def create_graphs(self):

        fig, ax = plt.subplots(figsize=(7, 3))

        # sns.boxplot(
        #     data=self.df,
        #     x='y',
        #     y='label',
        #     hue='label',
        #     whis=[0, 100],
        #     width=.6,
        #     palette="vlag"
        # )

        # ax.set(xlim=(0, 337))

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

        plt.show()


    def cluster(self):
        eps = 20
        min_samples = 1

        db = DBSCAN(eps=eps, min_samples=min_samples)
        db.fit(self.df)

        label_df = DataFrame({'label': db.labels_})

        self.df = pd.concat([self.df.reset_index(drop=True), label_df.reset_index(drop=True)], axis=1)

        print(self.df.to_csv('test.csv'))

        cluster_counts = self.df['label'].value_counts()

        multi_instance_clusters = cluster_counts[cluster_counts > 1].index

        filtered_df = self.df[self.df['label'].isin(multi_instance_clusters)]

        unique_labels = filtered_df['label'].unique()

        for i in range(len(unique_labels)):
            filtered_df['label'] = filtered_df['label'].replace(unique_labels[i], "Auto " + str(i + 1))

        self.df = filtered_df