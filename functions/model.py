from schema import sort_attributes

import keras
from keras import layers

import numpy as np
import tensorflow as tf

class Model:
    def __init__(self, attributes):
        self.model = None

        self.parameters = sort_attributes(attributes)

    def build_model(input_shape=51, num_actions=51):
        inputs = keras.Input(shape=(input_shape,))
        x = layers.Dense(64, activation="relu")(inputs)
        team1 = layers.Dense(num_actions)(x)
        team2 = layers.Dense(num_actions)(x)
        model = keras.Model(inputs, [team1, team2])
        return model