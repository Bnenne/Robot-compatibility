import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import random
import math

def generate_random_point():
    x = random.uniform(1, 5)
    y = random.uniform(1, 5)
    return {'x': x, 'y': y}

def generate_second_point(p1, distance):
    point = (p1.get('x'), p1.get('y'))
    while True:
        x2 = random.uniform(1, 5)
        y2 = random.uniform(1, 5)
        if math.dist(point, (x2, y2)) >= distance:
            return {'x': x2, 'y': y2}

distance = 1
point1 = generate_random_point()
point2 = generate_second_point(point1, distance)

# Parameters for the clusters
num_points = 50  # Number of points per cluster
cluster_1_center = [point1.get('x'), point1.get('y')]
cluster_2_center = [point2.get('x'), point2.get('y')]
spread = 0.25  # Spread of each cluster

# Generate random points around each cluster center
cluster_1 = np.random.normal(cluster_1_center, spread, (num_points, 2))
cluster_2 = np.random.normal(cluster_2_center, spread, (num_points, 2))

points = np.vstack([cluster_1, cluster_2])
labels = np.array([0] * num_points + [1] * num_points)

df = pd.DataFrame(points, columns=["x", "y"])
df['label'] = labels

# df.to_csv("training_data.csv", index=False)

# training_data = pd.read_csv('training_data.csv')

sns.set_theme(style='whitegrid')

sns.scatterplot(data=df, x='x', y='y', hue='label', palette='coolwarm')
plt.xlabel("X")
plt.ylabel("Y")
plt.title("Data Points Colored by Label")
plt.ylim(0, 6)
plt.xlim(0, 6)
plt.show()