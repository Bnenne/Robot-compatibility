from functions.define_team import define_team
from schema import sort_attributes

import keras
from keras import layers

class Model:
    def __init__(self,):
        self.model = None
        self.parameters = None
        self.team_cache = {}

    def build_model(self, input_shape=50, num_actions=50):
        inputs = keras.Input(shape=(input_shape,))
        x = layers.Dense(64, activation="relu")(inputs)
        team1 = layers.Dense(num_actions)(x)
        team2 = layers.Dense(num_actions)(x)
        self.model = keras.Model(inputs, [team1, team2])

    def create_parameters(self, team):
        if team not in self.team_cache:
            team_attributes = define_team(team)
            self.team_cache[team] = sort_attributes(team_attributes)

        self.parameters = self.team_cache[team]

    def predict(self, training=True):
        outputs = self.model(self.parameters, training=training)

        archetype_a = outputs[0]
        archetype_b = outputs[1]

        return archetype_a, archetype_b