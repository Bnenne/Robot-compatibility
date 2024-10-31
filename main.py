import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import requests

event_key = '2024wila'

teams = requests.get('https://www.thebluealliance.com/api/v3/event/'+event_key+'/teams/simple?X-TBA-Auth-Key=KBgtYZnVwKD4chpB2BkMxKbeyP00EijOvetrzzbporPZzs2ED1hAN7ceeTRnCui6')

r = requests.get('http://team1710scouting.vercel.app/api/'+event_key)

team_actions = []

for t in teams.json():
    team_actions.append({'team': t.get('team_number'), 'actions': []})

for t in team_actions:
    for s in r.json():
        for a in s.get('game').get('actions'):
            if s.get('team') == t.get('team'):
                t.get('actions').append(a)

def find_phase(list, team, phase):
    actions = []
    for o in list:
        if o.get('team') == team: 
            for a in o.get('actions'):
                if (a.get('phase') == phase) & (a.get('amplified') == True):
                    actions.append(a)
    return actions



print(find_phase(team_actions, 1710, 'teleOp'))
    

# data = pd.read_csv('finalized_combined.csv')

# red1 = data[['red1', 'red1_epa_pre_champs']]
# red1.rename(columns={'red1': 'teams', 'red1_epa_pre_champs': 'epa'}, inplace=True)

# red2 = data[['red2', 'red2_epa_pre_champs']]
# red2.rename(columns={'red2': 'teams', 'red2_epa_pre_champs': 'epa'}, inplace=True)

# red3 = data[['red3', 'red3_epa_pre_champs']]
# red3.rename(columns={'red3': 'teams', 'red3_epa_pre_champs': 'epa'}, inplace=True)

# blue1 = data[['blue1', 'blue1_epa_pre_champs']]
# blue1.rename(columns={'blue1': 'teams', 'blue1_epa_pre_champs': 'epa'}, inplace=True)

# blue2 = data[['blue2', 'blue2_epa_pre_champs']]
# blue2.rename(columns={'blue2': 'teams', 'blue2_epa_pre_champs': 'epa'}, inplace=True)

# blue3 = data[['blue3', 'blue3_epa_pre_champs']]
# blue3.rename(columns={'blue3': 'teams', 'blue3_epa_pre_champs': 'epa'}, inplace=True)

# teams = pd.concat([red1, red2, red3, blue1, blue2, blue3]).drop_duplicates('teams').sort_values('epa', ascending=False)

# teams = teams.sample(20)

# sns.set_theme(style='whitegrid')

# sns.barplot(x="epa", y="teams", data=teams, order=teams.sort_values('epa', ascending=False).teams,
#             label="EPA before Champs", color="b", orient='h')

# plt.show()