import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import requests
import json
import csv
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("API_KEY")

event_key = '2024ksla'

teams = requests.get('https://www.thebluealliance.com/api/v3/event/'+event_key+'/teams/simple?X-TBA-Auth-Key='+api_key)

r = requests.get('http://team1710scouting.vercel.app/api/'+event_key)

team_actions = []

for t in teams.json():
    team_actions.append({'team': t.get('team_number'), 'actions':{'auto':[], 'teleOp':[]}})

for t in team_actions:
    for s in r.json():
        for a in s.get('game').get('actions'):
            if s.get('team') == t.get('team'):
                if a.get('phase') == 'auto':
                    t.get('actions').get('auto').append(a)
                if a.get('phase') == 'teleOp':
                    t.get('actions').get('teleOp').append(a)

team_intake_prev = []

for t in team_actions:
    source = 0
    speaker = 0
    center = 0
    amp = 0
    trap = 0
    for i in t.get('actions').get('teleOp'):
        if i.get('action') == 'intake':
            match i.get('location'):
                case 'source':
                    source += 1
                case 'speaker':
                    speaker += 1
                case 'center':
                    center += 1
                case 'amp':
                    amp += 1
                case 'trap':
                    trap += 1
    team_intake_prev.append({'team': t.get('team'), 'source': source, 'speaker': speaker, 'center': center, 'amp': amp, 'trap': trap})

team_intake = []

for t in team_actions:
    source = 0
    speaker = 0
    center = 0
    amp = 0
    trap = 0
    for i in t.get('actions').get('teleOp'):
        if i.get('action') == 'intake':
            if i.get('location') == 'source':
                source += 1
            index = t.get('actions').get('teleOp').index(i)
            prev_action = t.get('actions').get('teleOp')[index - 1]
            if prev_action.get('action') == 'miss':
                print(index)
                print(t.get('actions').get('teleOp').index(prev_action))
                print(i)
                print(prev_action)
                print(' ')
                if prev_action.get('time') - i.get('time') > 5:
                    match i.get('location'):
                        case 'speaker':
                            speaker += 1
                        case 'center':
                            center += 1
                        case 'amp':
                            amp += 1
                        case 'trap':
                            trap += 1
    team_intake.append({'team': t.get('team'), 'source': source, 'speaker': speaker, 'center': center, 'amp': amp, 'trap': trap})

# print(team_intake_prev)
# print(team_intake)
# print(team_actions)

with open("team_intake_prev.json", "w") as outfile:
    json.dump(team_intake_prev, outfile, indent=4)

with open("team_intake.json", "w") as outfile:
    json.dump(team_intake, outfile, indent=4)

with open('team_intake_prev.json') as f:
    data1 = json.load(f)

# Open a CSV file for writing
with open('team_intake_prev.csv', 'w', newline='') as f:
    writer = csv.writer(f)

    # Write the header row (if the JSON data is an array of objects)
    if isinstance(data1, list):
        writer.writerow(data1[0].keys())

    # Write the data rows
    for row in data1:
        writer.writerow(row.values())

with open('team_intake.json') as f:
    data2 = json.load(f)

# Open a CSV file for writing
with open('team_intake.csv', 'w', newline='') as f:
    writer = csv.writer(f)

    # Write the header row (if the JSON data is an array of objects)
    if isinstance(data2, list):
        writer.writerow(data2[0].keys())

    # Write the data rows
    for row in data2:
        writer.writerow(row.values())

intake_data = pd.read_csv('team_intake_prev.csv')
intake_data_filtered = pd.read_csv('team_intake.csv')

# red1 = data[['red1', 'red1_epa_pre_champs']]
# red1.rename(columns={'red1': 'teams', 'red1_epa_pre_champs': 'epa'}, inplace=True)
#
# red2 = data[['red2', 'red2_epa_pre_champs']]
# red2.rename(columns={'red2': 'teams', 'red2_epa_pre_champs': 'epa'}, inplace=True)
#
# red3 = data[['red3', 'red3_epa_pre_champs']]
# red3.rename(columns={'red3': 'teams', 'red3_epa_pre_champs': 'epa'}, inplace=True)
#
# blue1 = data[['blue1', 'blue1_epa_pre_champs']]
# blue1.rename(columns={'blue1': 'teams', 'blue1_epa_pre_champs': 'epa'}, inplace=True)
#
# blue2 = data[['blue2', 'blue2_epa_pre_champs']]
# blue2.rename(columns={'blue2': 'teams', 'blue2_epa_pre_champs': 'epa'}, inplace=True)
#
# blue3 = data[['blue3', 'blue3_epa_pre_champs']]
# blue3.rename(columns={'blue3': 'teams', 'blue3_epa_pre_champs': 'epa'}, inplace=True)
#
# teams = pd.concat([red1, red2, red3, blue1, blue2, blue3]).drop_duplicates('teams').sort_values('epa', ascending=False)

sample_size = 20

intake_data = intake_data.sample(sample_size)
intake_data_filtered = intake_data_filtered.sample(sample_size)

sns.set_theme(style='whitegrid')

sns.barplot(x="source", y="team", data=intake_data_filtered,
            label="source", color="r", orient='h')

sns.barplot(x="speaker", y="team", data=intake_data_filtered,
            label="speaker", color="b", orient='h')

sns.barplot(x="center", y="team", data=intake_data_filtered,
            label="center", color="g", orient='h')

sns.barplot(x="amp", y="team", data=intake_data_filtered,
            label="amp", color="m", orient='h')

sns.barplot(x="trap", y="team", data=intake_data_filtered,
            label="trap", color="y", orient='h')

plt.show()