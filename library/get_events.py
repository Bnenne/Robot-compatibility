import requests, os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("API_KEY")

teams = requests.get('https://www.thebluealliance.com/api/v3/teams/2024/1/simple?X-TBA-Auth-Key='+api_key)

team_keys = []

for t in teams.json():
    team_keys.append(t['key'])

data = []

for team in team_keys:
    events = requests.get('https://www.thebluealliance.com/api/v3/team/'+team+'/events/2024?X-TBA-Auth-Key=' + api_key)
    event_keys = []
    for e in events.json():
        event_keys.append(e['key'])
    data.append({'key': team, 'events': event_keys})

print(data)