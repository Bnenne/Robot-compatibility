import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import random, math
from sklearn.cluster import MeanShift, estimate_bandwidth
from get_start import get_start_blue, get_start_red

# def generate_random_point():
#     x = random.uniform(-1, 1)
#     y = random.uniform(-1, 1)
#     return {'x': x, 'y': y}

# def generate_second_point(p1, distance):
#     point = (p1.get('x'), p1.get('y'))
#     while True:
#         x2 = random.uniform(-1, 1)
#         y2 = random.uniform(-1, 1)
#         if math.dist(point, (x2, y2)) >= distance:
#             return {'x': x2, 'y': y2}

# distance = (1/3)
# point1 = generate_random_point()
# point2 = generate_second_point(point1, distance)

# # Parameters for the clusters
# num_points = 50  # Number of points per cluster
# cluster_1_center = [point1.get('x'), point1.get('y')]
# cluster_2_center = [point2.get('x'), point2.get('y')]
# spread = (1/12)  # Spread of each cluster

# Generate random points around each cluster center
# cluster_1 = np.random.normal(cluster_1_center, spread, (num_points, 2))
# cluster_2 = np.random.normal(cluster_2_center, spread, (num_points, 2))

points_red = get_start_red(['2024ksla', '2024wila'], '1710')
points_blue = get_start_blue(['2024ksla', '2024wila'], '1710')

points_formatted_red = []
points_formatted_blue = []

for p in points_red:
    points_formatted_red.append([p['x'], p['y']])

for p in points_blue:
    points_formatted_blue.append([p['x'], p['y']])

print(points_formatted_red)
print(points_formatted_blue)

bandwidth_red = estimate_bandwidth(points_formatted_red, quantile=0.5)

ms_red = MeanShift(bandwidth=bandwidth_red, bin_seeding=True)
ms_red.fit(points_formatted_red)

df_red = pd.DataFrame(points_formatted_red, columns=["x", "y"])

bandwidth_blue = estimate_bandwidth(points_formatted_blue, quantile=0.5)

ms_blue = MeanShift(bandwidth=bandwidth_blue, bin_seeding=True)
ms_blue.fit(points_formatted_blue)

df_blue = pd.DataFrame(points_formatted_blue, columns=["x", "y"])

# df.to_csv("training_data.csv", index=False)

# training_data = pd.read_csv('training_data.csv')
print('Red')
print(df_red)
print(' ')
print('Blue')
print(df_blue)

sns.set_theme(style='whitegrid')

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

img_red = mpimg.imread('assets/red_starting.png')
img_blue = mpimg.imread('assets/blue_starting.png')

# Plot df_red on the first subplot
sns.scatterplot(data=df_red, x='x', y='y', hue=ms_red.labels_, palette='Reds', ax=ax1)
ax1.set_xlabel("X")
ax1.set_ylabel("Y")
ax1.set_title("Red Data Points")
ax1.set_ylim(0, 250)
ax1.set_xlim(0, 100)
ax1.imshow(img_red, extent=[0, 100, 0, 250])

# Plot df_blue on the second subplot
sns.scatterplot(data=df_blue, x='x', y='y', hue=ms_blue.labels_, palette='Blues_d', ax=ax2)
ax2.set_xlabel("X")
ax2.set_ylabel("Y")
ax2.set_title("Blue Data Points")
ax2.set_ylim(0, 250)
ax2.set_xlim(0, 100)
ax2.imshow(img_blue, extent=[0, 100, 0, 250])

# Display the plot
plt.suptitle("Data Points Colored by Label (Separate Subplots)")
plt.tight_layout()
plt.show()