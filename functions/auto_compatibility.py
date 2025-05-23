import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN, KMeans
from functions.scouting_api import ScoutingAPI
import io, math
from itertools import combinations

class DataLabeling:
    def __init__(self, event_key, team_key):
        """Initializes the DataLabeling class with the given event key and team key

        Args:
            event_key (str): The event key (e.g., '2025cttd') or 'events' for all events
            team_key (str): The team key (e.g., 'frc1710')
        """
        self.event_key = event_key
        self.team_key = team_key
        sa = ScoutingAPI(self.event_key, self.team_key)

        points = sa.starts()

        print('points', points)

        points_formatted = []
        points_formatted_to_label = []

        for p in points:
            points_formatted_to_label.append([p['x'], p['y']])
            points_formatted.append([
                p['x'],
                p['y'],
                p['auto_score'],
                p['team'],
                p['processor'],
                p['coral_station'],
                p['reef'],
                p['alliance'],
                p['barge']
            ])

        eps = 25
        min_samples = 1
        print('points_formatted_to_label', points_formatted_to_label)
        db = DBSCAN(eps=eps, min_samples=min_samples)
        db.fit(points_formatted_to_label)

        df = pd.DataFrame(points_formatted,
                          columns=[
                              "x",
                              "y",
                              "auto_score",
                              "team",
                              'processor',
                              'coral_station',
                              'reef',
                              'alliance',
                              'barge'
                          ])

        sns.set_theme(style='whitegrid')

        self.img_blue = plt.imread('functions/assets/starting_map.png')

        df_copy = df
        print('df_copy', df_copy)
        print('db.labels_', db.labels_)
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
            op = KMeans(n_clusters=1)
            op.fit(labelless_data)
            i = 0
            for p in self.df.to_dict(orient='records'):
                new_data.append([
                    p['x'],
                    p['y'],
                    p['auto_score'],
                    p['team'],
                    p['processor'],
                    p['coral_station'],
                    p['reef'],
                    p['alliance'],
                    p['barge'],
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
                                  "label",
                                  'processor',
                                  'coral_station',
                                  'reef',
                                  'alliance',
                                  'barge'
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
            processor = 0
            coral_station = 0
            reef = 0
            alliance = 0
            barge = 0
            for a in self.df.to_dict(orient='records'):
                if a['label'] == l['label']:
                    l['points'].append(a)
                    processor += a['processor']
                    coral_station += a['coral_station']
                    reef += a['reef']
                    alliance += a['alliance']
                    barge += a['barge']
            for e in l['points']:
                sample += 1
                x += e['x']
                y += e['y']
                auto_score += e['auto_score']
            x_mass = x/sample
            y_mass = y/sample
            processor_mass = processor/sample
            coral_mass = coral_station/sample
            reef_mass = reef/sample
            alliance_mass = alliance/sample
            barge_mass = barge/sample
            auto_mass = auto_score/sample
            masses.append({'x': x_mass, 'y': y_mass, 'auto_score': auto_mass, 'team': team, 'label': l['label'],'processor': processor_mass, 'coral_station': coral_mass, 'reef': reef_mass, 'alliance': alliance_mass, 'barge': barge_mass})

        self.df_masses = pd.DataFrame(masses,
                          columns=[
                              "x",
                              "y",
                              "auto_score",
                              "team",
                              "label",
                              "processor",
                              "coral_station",
                              "reef",
                              "alliance",
                              "barge"
                          ])
    def return_graph(self, title):
        """Generates a scatter plot graph for the labeled data and mass points.

        Args:
            title (str): The title for the graph.

        Returns:
            io.BytesIO: A buffer containing the saved graph image in PNG format.
        """
        fig, axes = plt.subplots(1, 2, figsize=(4, 8))

        print('self.df', self.df)
        print('self.df_masses', self.df_masses)

        sns.scatterplot(
            data=self.df,
            x='x',
            y='y',
            hue=self.labels,
            palette='Accent',
            size='auto_score',
            legend=False,
            ax=axes[0]
        )
        axes[0].set_xlabel("X")
        axes[0].set_ylabel("Y")
        axes[0].set_xlim(-1, 1)
        axes[0].set_ylim(0, 337)

        sns.scatterplot(
            data=self.df_masses,
            x='x',
            y='y',
            hue='label',
            palette='Accent',
            size='auto_score',
            legend=False,
            ax=axes[1]
        )

        axes[1].set_xlabel("X")
        axes[1].set_ylabel("Y")
        axes[1].set_xlim(-1, 1)
        axes[1].set_ylim(0, 337)

        plt.suptitle(title)
        plt.tight_layout()

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plt.close()

        return buf
    def return_data(self):
        """Returns the labeled data and mass points as dictionaries.

        Returns:
            dict: A dictionary containing the general labeled data and mass points.
        """
        return {'general': self.df.to_dict(), 'masses': self.df_masses.to_dict()}

class Compare:
    def __init__(self, event_key, team_key):
        """Initializes the Compare class with the given event key and team keys.

        Args:
            event_key (str): The event key (e.g., '2025cttd') or 'events' for all events
            team_key (list): A list of team keys (e.g., ['frc1710', 'frc1234'])
        """
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

        self.general_confidence = pd.DataFrame(columns=[
                                      "x",
                                      "y",
                                      "auto_score",
                                      "team",
                                      "label"
                                  ])
        self.masses_confidence = pd.DataFrame(columns=[
                                      "x",
                                      "y",
                                      "auto_score",
                                      "team",
                                      "label"
                                  ])

        for d in self.data:
            general_confidence = pd.DataFrame(d['general'],
                                  columns=[
                                      "x",
                                      "y",
                                      "auto_score",
                                      "team",
                                      "label"
                                  ])
            self.general_confidence = pd.concat([self.general_confidence, general_confidence])
            masses_confidence = pd.DataFrame(d['masses'],
                                              columns=[
                                                  "x",
                                                  "y",
                                                  "auto_score",
                                                  "team",
                                                  "label"
                                              ])
            self.masses_confidence = pd.concat([self.masses_confidence, masses_confidence])

        self.masses_confidence = self.masses_confidence.to_dict(orient='records')
        self.general_confidence = self.general_confidence.to_dict(orient='records')

        self.confidences = []

        print(self.masses_confidence)
        print(self.general_confidence)

        for m in self.masses_confidence:
            confidences = []
            for g in self.general_confidence:
                if g['team'] == m['team'] and g['label'] == m['label']:
                    x = g['x'] - m['x']
                    y = g['y'] - m['y']
                    confidences.append(math.sqrt((x*x)+(y*y)))
            self.confidences.append({'confidences': confidences, 'team': m['team']})

        print('confidences', self.confidences)

        self.i = 0
        self.total = 0

        for c in self.confidences:
            i = 0
            total = 0
            for a in c['confidences']:
                i += 1
                confidence = (50-a)/50
                if confidence < 0:
                    confidence = 0
                total += confidence
            self.i += 1
            self.total += total / i

        starting_confidence = self.total / self.i

        print('starting_confidence', starting_confidence)

        confidence_teams = []
        confidence_team = []

        for g in self.general_confidence:
            team = str(g['team'])
            if g['team'] not in confidence_teams:
                confidence_teams.append(g['team'])
                confidence_team.append({team: 0})
            for c in confidence_team:
                try:
                    c[team] += 1
                except:
                    pass

        for c in confidence_team:
            team = ""
            for key, value in c.items():
                team = key
            confidence = c[team]/30
            if confidence > 1:
                confidence = 1
            c[team] = confidence

        self.i = 0
        self.data_confidence = 0

        for c in confidence_team:
            team = ""
            for key, value in c.items():
                team = key
            self.i += 1
            self.data_confidence += c[team]

        self.data_confidence = self.data_confidence / self.i

        print('data_confidence', self.data_confidence)

        self.confidence = (self.data_confidence*0.5)+(starting_confidence*0.5)

        print('confidence', self.confidence)

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

        eps = 100
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

        self.theoretical_max = 0
        team_max = []

        for t in teams_single:
            highestAuto = 0
            for e in self.combined_data.to_dict(orient='records'):
                if e['team'] == t:
                    if e['auto_score'] > highestAuto:
                        highestAuto = e['auto_score']
            self.theoretical_max += highestAuto
            team_max.append({'team': t, 'max': highestAuto})

        print(team_max)
        print(self.theoretical_max)

        print(self.combined_data.to_dict(orient='records'))

        change = 0

        def get_max():
            combination = combinations(self.combined_data.to_dict(orient='records'), len(teams_single) - change)

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
            print("valid entries", valid_entries)
            for valid_entry in valid_entries:
                print("valid entry", valid_entry)

            m = 0

            mp = None

            for v in valid_entries:
                if len(teams_single) - change == 2:
                    score = v[0]['auto_score'] + v[1]['auto_score']
                    if score > m:
                        m = score
                        mp = v
                if len(teams_single) - change == 3:
                    score = v[0]['auto_score'] + v[1]['auto_score'] + v[2]['auto_score']
                    if score > m:
                        m = score
                        mp = v

            return m, mp

        self.max, self.maxPos = get_max()
        if self.maxPos is None:
            change = 1
            self.max, self.maxPos = get_max()
        if self.maxPos is None:
            change = 2
            self.max, self.maxPos = get_max()

        # maxPos_len = len(list(self.maxPos))

        print('self.max', self.max)

        print('self.maxPos', self.maxPos)

        self.maxPos = pd.DataFrame(list(self.maxPos),
                              columns=['x', 'y', 'auto_score', 'team', 'label']
                              )

        self.compatibility = (self.max / self.theoretical_max) * 100

        name = str(round(self.compatibility, 2)) + "%"

        self.compatibility_data = {'name': name, 'compatibility': self.compatibility}

        self.compatibility_data = pd.DataFrame(self.compatibility_data, index=[0])

        print('compatibility_data', self.compatibility_data)

    def return_compare_graph(self, title):
        """Generates a comparison graph for the teams and their compatibility.

        Args:
            title (str): The title for the graph.

        Returns:
            io.BytesIO: A buffer containing the saved comparison graph image in PNG format.
        """
        team_length = len(self.team_key)

        fig, axes = plt.subplots((1 * team_length) + 1, 2, figsize=(4, team_length + 8))

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
                palette='Accent',
                size='auto_score',
                legend=False,
                ax=axes[i, 0]
            )
            axes[i, 0].set_xlabel("X")
            axes[i, 0].set_ylabel("Y")
            axes[i, 0].set_xlim(-1, 1)
            axes[i, 0].set_ylim(0, 337)

            sns.scatterplot(
                data=masses,
                x='x',
                y='y',
                hue='label',
                palette='Accent',
                size='auto_score',
                legend=False,
                ax=axes[i, 1]
            )
            axes[i, 1].set_xlabel("X")
            axes[i, 1].set_ylabel("Y")
            axes[i, 1].set_xlim(-1, 1)
            axes[i, 1].set_ylim(0, 337)
            i += 1

        sns.scatterplot(
            data=self.maxPos,
            x='x',
            y='y',
            hue='label',
            palette='Accent',
            size='auto_score',
            legend=False,
            ax=axes[i, 0]
        )
        axes[i, 0].set_xlabel("X")
        axes[i, 0].set_ylabel("Y")
        axes[i, 0].set_xlim(-1, 1)
        axes[i, 0].set_ylim(0, 337)

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
        """Returns the comparison data for the teams, including compatibility and theoretical maximum.

        Returns:
            dict: A dictionary containing the teams' data, combined maximum positions, compatibility percentage, theoretical maximum, and realistic maximum.
        """
        return {'teams': self.data, 'combined': self.maxPos.to_dict(orient='records'), 'compatibility': self.compatibility, 'theoretical': self.theoretical_max, 'realistic': self.max}