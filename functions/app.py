import os

os.environ["KERAS_BACKEND"] = "tensorflow"

from define_team import define_team
from model import Model

team = 1710

team_attributes = define_team(team)

model = Model(team_attributes)