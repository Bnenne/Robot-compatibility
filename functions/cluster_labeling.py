import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
from functions.scouting_api import ScoutingAPI
import io

class DataLabeling:
    def __init__(self, event_key, team_key):
        self.event_key = event_key
        self.team_key = team_key
        sa = ScoutingAPI(event_key, team_key)

        points_red = sa.get_start_red()
        points_blue = sa.get_start_blue()

        points = []

        for p in points_red:
            points.append(p)

        for p in points_blue:
            points.append(p)

        points_formatted = []
        points_formatted_to_label = []

        for p in points:
            points_formatted_to_label.append([p['x'], p['y']])
            points_formatted.append([
                p['x'],
                p['y'],
                # p['strat'],
                p['auto_score']
            ])

        eps = 25
        min_samples = 1

        db = DBSCAN(eps=eps, min_samples=min_samples)
        db.fit(points_formatted_to_label)

        df = pd.DataFrame(points_formatted,
                          columns=[
                              "x",
                              "y",
                              # "strat",
                              "auto_score"
                          ])

        sns.set_theme(style='whitegrid')

        self.img_blue = plt.imread('functions/assets/starting_map.png')

        df_copy = df
        df_copy['label'] = db.labels_

        # print(df)
        # print(df_copy)

        labels_array = np.array(db.labels_)

        unique_labels = np.unique(labels_array)

        if len(unique_labels) > 3:
            unique_labels, counts = np.unique(labels_array, return_counts=True)
            single_occurrence_labels = unique_labels[counts == 1]

            mask = ~np.isin(labels_array, single_occurrence_labels)
            filtered_labels = labels_array[mask]

            unique_labels = df_copy['label'].value_counts()
            single_labels = unique_labels[unique_labels == 1].index

            df_filtered = df_copy[~df_copy['label'].isin(single_labels)]
        else:
            filtered_labels = labels_array
            df_filtered = df_copy
        self.labels = filtered_labels
        self.df = df_filtered

        self.labels_single = {item["label"] for item in self.df.to_dict(orient='records')}

        self.labels_single = list(self.labels_single)

        self.grouped_labels = []

        for l in self.labels_single:
            self.grouped_labels.append({'label': int(l), 'points': []})

        self.masses = []

        for l in self.grouped_labels:
            x = 0
            y = 0
            auto_score = 0
            sample = 0
            for a in self.df.to_dict(orient='records'):
                if a['label'] == l['label']:
                    l['points'].append(a)
            for e in l['points']:
                sample += 1
                x += e['x']
                y += e['y']
                auto_score += e['auto_score']
            x_mass = x/sample
            y_mass = y/sample
            auto_mass = auto_score/sample
            self.masses.append({'x': x_mass, 'y': y_mass, 'auto_score': auto_mass, 'label': l['label']})

        self.df_masses = pd.DataFrame(self.masses,
                          columns=[
                              "x",
                              "y",
                              "auto_score",
                              "label"
                          ])

        # print(self.df_masses)
    def return_graph(self):
        fig, axes = plt.subplots(1, 2)

        sns.scatterplot(
            data=self.df,
            x='x',
            y='y',
            hue=self.labels,
            palette='CMRmap',
            size='auto_score',
            legend=False,
            ax=axes[0]
        )
        axes[0].set_xlabel("X")
        axes[0].set_ylabel("Y")
        axes[0].set_xlim(0, 100)
        axes[0].set_ylim(0, 250)
        axes[0].imshow(self.img_blue, extent=[0, 100, 0, 250])

        sns.scatterplot(
            data=self.df_masses,
            x='x',
            y='y',
            hue='label',
            palette='CMRmap',
            size='auto_score',
            legend=False,
            ax=axes[1]
        )

        axes[1].set_xlabel("X")
        axes[1].set_ylabel("Y")
        axes[1].set_xlim(0, 100)
        axes[1].set_ylim(0, 250)
        axes[1].imshow(self.img_blue, extent=[0, 100, 0, 250])

        title = self.event_key + " " + self.team_key

        plt.suptitle(title)
        plt.tight_layout()
        # plt.show()

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plt.close()

        return buf
    def return_data(self):
        return {'general': self.df.to_dict(), 'masses': self.df_masses.to_dict()}