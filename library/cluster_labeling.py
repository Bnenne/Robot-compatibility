import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
from get_start import get_start_blue, get_start_red

event_keys = ['2024ksla', '2024wila', '2024dal', '2024cttd']
team_key = '1710'

# event_keys = ['2024oktu', '2024ksla', '2024mokc', '2024mil', '2024mksc']
# team_key = '1730'

# event_keys = ['2024ksla', '2024ilch', '2024dal', '2024mksc', '2024cttd']
# team_key = '1986'

points_red = get_start_red(event_keys, team_key)
points_blue = get_start_blue(event_keys, team_key)

points = []

for p in points_red:
    points.append(p)

for p in points_blue:
    points.append(p)

points_formatted = []

for p in points:
    points_formatted.append([p['x'], p['y']])

eps = 25
min_samples = 1

db = DBSCAN(eps=eps, min_samples=min_samples)
db.fit(points_formatted)

df = pd.DataFrame(points_formatted, columns=["x", "y"])

sns.set_theme(style='whitegrid')

img_blue = plt.imread('assets/starting_map.png')

df_copy = df
df_copy['label'] = db.labels_

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

sns.scatterplot(data=df_filtered, x='x', y='y', hue=filtered_labels, palette='CMRmap', legend=None)
plt.xlabel("X")
plt.ylabel("Y")
plt.ylim(0, 250)
plt.xlim(0, 100)
plt.imshow(img_blue, extent=[0, 100, 0, 250])

keys = ''

for e in event_keys:
    keys = keys + e + ' '

title = keys + team_key + ' ' + str(eps)

plt.suptitle(title)
plt.tight_layout()
plt.show()