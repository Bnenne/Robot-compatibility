import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from sklearn.cluster import MeanShift, estimate_bandwidth
from scouting_api import scoutingAPI

event_keys = ['2024ksla', '2024wila']
team_key = '1710'

sa = scoutingAPI(event_keys, team_key)

points_red = sa.get_start_red()
points_blue = sa.get_start_blue()

print(points_blue)
print(points_red)

points_formatted_red = []
points_formatted_blue = []
 
for p in points_red:
    points_formatted_red.append([p['x'], p['y'], p['strat']])

for p in points_blue:
    points_formatted_blue.append([p['x'], p['y'], p['strat']])

print(points_formatted_red)
print(points_formatted_blue)

bandwidth_red = estimate_bandwidth(points_formatted_red, quantile=0.5)

ms_red = MeanShift(bandwidth=bandwidth_red, bin_seeding=True)
ms_red.fit(points_formatted_red)

df_red = pd.DataFrame(points_formatted_red, columns=["x", "y", "strat"])

bandwidth_blue = estimate_bandwidth(points_formatted_blue, quantile=0.5)

ms_blue = MeanShift(bandwidth=bandwidth_blue, bin_seeding=True)
ms_blue.fit(points_formatted_blue)

df_blue = pd.DataFrame(points_formatted_blue, columns=["x", "y", "strat"])

print('Red')
print(df_red)
print(' ')
print('Blue')
print(df_blue)

sns.set_theme(style='whitegrid')

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

img_red = mpimg.imread('assets/red_starting.png')
img_blue = mpimg.imread('assets/blue_starting.png')

sns.scatterplot(data=df_red, x='x', y='y', hue=ms_red.labels_, palette='Reds', size='strat', ax=ax1)
ax1.set_xlabel("X")
ax1.set_ylabel("Y")
ax1.set_title("Red Data Points")
ax1.set_ylim(0, 250)
ax1.set_xlim(0, 100)
ax1.imshow(img_red, extent=[0, 100, 0, 250])

sns.scatterplot(data=df_blue, x='x', y='y', hue=ms_blue.labels_, palette='Blues_d', size='strat', ax=ax2)
ax2.set_xlabel("X")
ax2.set_ylabel("Y")
ax2.set_title("Blue Data Points")
ax2.set_ylim(0, 250)
ax2.set_xlim(0, 100)
ax2.imshow(img_blue, extent=[0, 100, 0, 250])

plt.suptitle("Data Points Colored by Label (Separate Subplots)")
plt.tight_layout()
plt.show()