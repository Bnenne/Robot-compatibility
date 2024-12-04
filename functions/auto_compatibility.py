import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN, KMeans
from functions.scouting_api import ScoutingAPI
import io
from itertools import combinations

class DataLabeling:
    def __init__(self, event_key, team_key):
        self.event_key = event_key
        self.team_key = team_key
        sa = ScoutingAPI(self.event_key, self.team_key)

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
                p['auto_score'],
                p['team']
            ])

        eps = 25
        min_samples = 1

        db = DBSCAN(eps=eps, min_samples=min_samples)
        db.fit(points_formatted_to_label)

        df = pd.DataFrame(points_formatted,
                          columns=[
                              "x",
                              "y",
                              "auto_score",
                              "team"
                          ])

        sns.set_theme(style='whitegrid')

        self.img_blue = plt.imread('functions/assets/starting_map.png')

        df_copy = df
        df_copy['label'] = db.labels_

        labels_array = np.array(db.labels_)

        unique_labels = np.unique(labels_array)

        if len(unique_labels) > 2:
            unique_labels, counts = np.unique(labels_array, return_counts=True)
            single_occurrence_labels = unique_labels[counts <= 2]

            mask = ~np.isin(labels_array, single_occurrence_labels)
            filtered_labels = labels_array[mask]

            unique_labels = df_copy['label'].value_counts()
            single_labels = unique_labels[unique_labels <= 2].index

            df_filtered = df_copy[~df_copy['label'].isin(single_labels)]
        else:
            filtered_labels = labels_array
            df_filtered = df_copy
        self.labels = filtered_labels
        self.df = df_filtered

        labels_array = np.array(filtered_labels)

        unique_labels = np.unique(labels_array)

        labelless_data = []
        new_data = []

        if len(unique_labels) == 1:
            for p in self.df.to_dict(orient='records'):
                labelless_data.append([p['x'], p['y']])
            op = KMeans(n_clusters=2)
            op.fit(labelless_data)
            i = 0
            for p in self.df.to_dict(orient='records'):
                new_data.append([
                    p['x'],
                    p['y'],
                    p['auto_score'],
                    p['team'],
                    int(op.labels_[i])
                ])
                i += 1
            print(new_data)
            self.df = pd.DataFrame(new_data,
                              columns=[
                                  "x",
                                  "y",
                                  "auto_score",
                                  "team",
                                  "label"
                              ])
            self.labels = op.labels_

        print(self.df)

        labels_single = {item["label"] for item in self.df.to_dict(orient='records')}

        labels_single = list(labels_single)

        grouped_labels = []

        for l in labels_single:
            grouped_labels.append({'label': int(l), 'points': []})

        masses = []

        team = None

        for a in self.df.to_dict(orient='records'):
            team = a['team']
            break

        for l in grouped_labels:
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
            masses.append({'x': x_mass, 'y': y_mass, 'auto_score': auto_mass, 'team': team, 'label': l['label']})

        self.df_masses = pd.DataFrame(masses,
                          columns=[
                              "x",
                              "y",
                              "auto_score",
                              "team",
                              "label"
                          ])
    def return_graph(self, title):
        fig, axes = plt.subplots(1, 2, figsize=(6, 5))

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

        plt.suptitle(title)
        plt.tight_layout()

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plt.close()

        return buf
    def return_data(self):
        return {'general': self.df.to_dict(), 'masses': self.df_masses.to_dict()}

class Compare:
    def __init__(self, event_key, team_key):
        self.event_key = event_key
        self.team_key = team_key
        self.img_blue = plt.imread('functions/assets/starting_map.png')

        self.data = []

        teams = ""

        for t in self.team_key:
            teams = teams + " " + t
            dl = DataLabeling(self.event_key, t)
            self.data.append(dl.return_data())

        print(self.data)

        i = 0

        self.combined_data = None

        for d in self.data:
            masses = pd.DataFrame(d['masses'],
                                  columns=[
                                      "x",
                                      "y",
                                      "auto_score",
                                      "team",
                                      "label"
                                  ])
            if i == 0:
                self.combined_data = masses
            if i != 0:
                self.combined_data = pd.concat([self.combined_data, masses])
            i += 1

        to_label = []
        for d in self.combined_data.to_dict(orient='records'):
            to_label.append([
                d['x'],
                d['y']
            ])

        eps = 40
        min_samples = 1
        db = DBSCAN(eps=eps, min_samples=min_samples)
        db.fit(to_label)

        self.combined_data['label'] = db.labels_.tolist()

        teams_single = []

        for e in self.combined_data.to_dict(orient='records'):
            if e['team'] in teams_single:
                pass
            else:
                teams_single.append(e['team'])

        theoretical_max = 0
        team_max = []

        for t in teams_single:
            highestAuto = 0
            for e in self.combined_data.to_dict(orient='records'):
                if e['team'] == t:
                    if e['auto_score'] > highestAuto:
                        highestAuto = e['auto_score']
            theoretical_max += highestAuto
            team_max.append({'team': t, 'max': highestAuto})

        print(team_max)
        print(theoretical_max)

        print(self.combined_data.to_dict(orient='records'))

        combination = combinations(self.combined_data.to_dict(orient='records'), len(teams_single))

        valid_entries = []

        for entry in combination:
            teams_seen = set()
            labels_seen = set()
            is_valid = True
            for dict_item in entry:
                team = dict_item['team']
                label = dict_item['label']

                if team in teams_seen or label in labels_seen:
                    is_valid = False
                    break
                teams_seen.add(team)
                labels_seen.add(label)
            if is_valid:
                valid_entries.append(entry)

        # Print the valid entries
        for valid_entry in valid_entries:
            print(valid_entry)

        max = 0
        self.maxPos = None

        for v in valid_entries:
            if len(teams_single) == 2:
                score = v[0]['auto_score'] + v[1]['auto_score']
                if score > max:
                    max = score
                    maxPos = v
            if len(teams_single) == 3:
                score = v[0]['auto_score'] + v[1]['auto_score'] + v[2]['auto_score']
                if score > max:
                    max = score
                    maxPos = v

        print(max)

        self.maxPos = pd.DataFrame(list(maxPos),
                              columns=['x', 'y', 'auto_score', 'team', 'label']
                              )

        self.compatibility = (max / theoretical_max) * 100

        name = str(round(self.compatibility, 2)) + "%"

        self.compatibility_data = {'name': name, 'compatibility': self.compatibility}

        self.compatibility_data = pd.DataFrame(self.compatibility_data, index=[0])

        print('compatibility_data', self.compatibility_data)

    def return_compare_graph(self, title):
        team_length = len(self.team_key)

        fig, axes = plt.subplots((1 * team_length) + 1, 2, figsize=(6, (5 * team_length) + 5))

        i = 0

        for d in self.data:
            general = pd.DataFrame(d['general'],
                                   columns=[
                                       "x",
                                       "y",
                                       "auto_score",
                                       "team",
                                       "label"
                                   ])
            masses = pd.DataFrame(d['masses'],
                                  columns=[
                                      "x",
                                      "y",
                                      "auto_score",
                                      "team",
                                      "label"
                                  ])

            sns.scatterplot(
                data=general,
                x='x',
                y='y',
                hue='label',
                palette='CMRmap',
                size='auto_score',
                legend=False,
                ax=axes[i, 0]
            )
            axes[i, 0].set_xlabel("X")
            axes[i, 0].set_ylabel("Y")
            axes[i, 0].set_xlim(0, 100)
            axes[i, 0].set_ylim(0, 250)
            axes[i, 0].imshow(self.img_blue, extent=[0, 100, 0, 250])

            sns.scatterplot(
                data=masses,
                x='x',
                y='y',
                hue='label',
                palette='CMRmap',
                size='auto_score',
                legend=False,
                ax=axes[i, 1]
            )
            axes[i, 1].set_xlabel("X")
            axes[i, 1].set_ylabel("Y")
            axes[i, 1].set_xlim(0, 100)
            axes[i, 1].set_ylim(0, 250)
            axes[i, 1].imshow(self.img_blue, extent=[0, 100, 0, 250])
            i += 1

        sns.scatterplot(
            data=self.maxPos,
            x='x',
            y='y',
            hue='label',
            palette='CMRmap',
            size='auto_score',
            legend=False,
            ax=axes[i, 0]
        )
        axes[i, 0].set_xlabel("X")
        axes[i, 0].set_ylabel("Y")
        axes[i, 0].set_xlim(0, 100)
        axes[i, 0].set_ylim(0, 250)
        axes[i, 0].imshow(self.img_blue, extent=[0, 100, 0, 250])

        sns.barplot(
            data=self.compatibility_data,
            x='name',
            y='compatibility',
            legend=False,
            ax=axes[i, 1]
        )
        axes[i, 1].set_xlabel("")
        axes[i, 1].set_ylabel("Compatibility %")
        axes[i, 1].set_ylim(0, 100)

        plt.suptitle(title)
        plt.tight_layout()

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plt.close()

        return buf
    def return_compare_data(self):
        return {'teams': self.data, 'combined': self.maxPos.to_dict(orient='records'), 'compatibility': self.compatibility}