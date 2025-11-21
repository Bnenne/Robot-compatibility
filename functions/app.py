import os

import keras

os.environ["KERAS_BACKEND"] = "tensorflow"
os.environ["LOKY_MAX_CPU_COUNT"] = "8"

from model import Model
from train import Trainer
from functions.define_team import get_teams

epochs = 50
optimizer = keras.optimizers.Adam(learning_rate=0.001)

model = Model()
model.build_model(50, 50)

teams = get_teams()

trainer = Trainer(model, optimizer, teams)
trainer.train(epochs)