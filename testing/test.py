import os

os.environ["KERAS_BACKEND"] = "tensorflow"
os.environ["LOKY_MAX_CPU_COUNT"] = "8"

from training.define_team import get_teams, define_team
from training.schema import sort_attributes
from tensorflow.keras.models import load_model
import tensorflow as tf
import numpy as np
from numpy.linalg import norm

team_cache = {}

teams = get_teams()

for i, team in enumerate(teams):
    team_attributes = define_team(team)
    team_attributes = sort_attributes(team_attributes)
    team_cache[team] = team_attributes

    if (i + 1) % 10 == 0:  # Print every 10 teams
        print(f"Team {i + 1}/{len(teams)}")

model = load_model('C:/Users/bnenn/PycharmProjects/python-data-processing/model.h5')

outputs = model.predict(team_cache[1710])

archetype_a, archetype_b = outputs

archetype_a = tf.tanh(archetype_a)
archetype_b = tf.tanh(archetype_b)

def cosine_similarity(a, b):
    return np.dot(a, b) / (norm(a) * norm(b))

def best_vector_match(archetype_vec, team_cache):
    best_team = None
    best_score = -999

    for team, attrs in team_cache.items():
        attrs_vec = np.array(attrs).flatten()
        score = cosine_similarity(archetype_vec, attrs_vec)
        if score > best_score:
            best_score = score
            best_team = team

    return best_team

archetype_a = archetype_a.numpy().flatten()
archetype_b = archetype_b.numpy().flatten()

best_match_a = best_vector_match(archetype_a, team_cache)
best_match_b = best_vector_match(archetype_b, team_cache)

match_a_team = team_cache[best_match_a]
match_b_team = team_cache[best_match_b]

print(best_match_a, match_a_team)
print(best_match_b, match_b_team)