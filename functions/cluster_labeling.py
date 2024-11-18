import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
from functions.scouting_api import ScoutingAPI
import io

def return_graph(event_key, team_key):
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
        points_formatted.append([p['x'], p['y'], p['strat']])

    eps = 25
    min_samples = 1

    db = DBSCAN(eps=eps, min_samples=min_samples)
    db.fit(points_formatted_to_label)

    df = pd.DataFrame(points_formatted, columns=["x", "y", "strat"])

    sns.set_theme(style='whitegrid')

    img_blue = plt.imread('functions/assets/starting_map.png')

    df_copy = df
    df_copy['label'] = db.labels_

    print(df)
    print(df_copy)

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

    sns.scatterplot(data=df_filtered, x='x', y='y', hue=filtered_labels, palette='CMRmap', size='strat')
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.ylim(0, 250)
    plt.xlim(0, 100)
    plt.imshow(img_blue, extent=[0, 100, 0, 250])

    title = event_key[0] + team_key

    plt.suptitle(title)
    plt.tight_layout()
    # plt.show()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()

    return buf

def return_data(event_key, team_key):
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
        points_formatted.append([p['x'], p['y'], p['strat']])

    eps = 25
    min_samples = 1

    db = DBSCAN(eps=eps, min_samples=min_samples)
    db.fit(points_formatted_to_label)

    df = pd.DataFrame(points_formatted, columns=["x", "y", "strat"])

    sns.set_theme(style='whitegrid')

    img_blue = plt.imread('functions/assets/starting_map.png')

    df_copy = df
    df_copy['label'] = db.labels_

    print(df)
    print(df_copy)

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

    return df_filtered.to_dict()