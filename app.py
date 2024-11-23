# import pandas as pd
# import seaborn as sns
# import matplotlib.pyplot as plt
# from functions.intake_locations import create_files

# create_files()

# intake_data = pd.read_csv('team_intake_prev.csv')
# intake_data_filtered = pd.read_csv('team_intake.csv')

# sample_size = 20

# intake_data = intake_data.sample(sample_size)
# intake_data_filtered = intake_data_filtered.sample(sample_size)

# sns.set_theme(style='whitegrid')

# sns.barplot(x="source", y="team", data=intake_data_filtered,
#             label="source", color="r", orient='h')

# sns.barplot(x="speaker", y="team", data=intake_data_filtered,
#             label="speaker", color="b", orient='h')

# sns.barplot(x="center", y="team", data=intake_data_filtered,
#             label="center", color="g", orient='h')

# sns.barplot(x="amp", y="team", data=intake_data_filtered,
#             label="amp", color="m", orient='h')

# sns.barplot(x="trap", y="team", data=intake_data_filtered,
#             label="trap", color="y", orient='h')

# plt.show()

from flask import Flask, jsonify, send_file
from functions.cluster_labeling import DataLabeling
import json

# create_files()
  
app = Flask(__name__) 

@app.route("/graph/<event>/<team>", methods=['GET']) 
def get_graph(event, team):
    dl = DataLabeling(event, team)
    return send_file(dl.return_graph(), mimetype='image/png'), 200

@app.route("/data/<event>/<team>", methods=['GET'])
def get_data(event, team):
    dl = DataLabeling(event, team)
    return jsonify(dl.return_data()), 200
  
if __name__ == "__main__": 
    app.run(debug=True)