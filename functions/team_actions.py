import requests
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("API_KEY")

event_key = '2024ksla'

teams = requests.get('https://www.thebluealliance.com/api/v3/event/'+event_key+'/teams/simple?X-TBA-Auth-Key='+api_key)

r = requests.get('http://team1710scouting.vercel.app/api/'+event_key)

actions = []

for t in teams.json():
    actions.append({'team': t.get('team_number'), 'actions':{'auto':[], 'teleOp':[]}})

for t in actions:
    for s in r.json():
        for a in s.get('game').get('actions'):
            if s.get('team') == t.get('team'):
                if a.get('phase') == 'auto':
                    t.get('actions').get('auto').append(a)
                if a.get('phase') == 'teleOp':
                    t.get('actions').get('teleOp').append(a)