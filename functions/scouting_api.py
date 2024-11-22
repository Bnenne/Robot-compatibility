import requests, os, json
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("API_KEY")

# teams = requests.get('https://www.thebluealliance.com/api/v3/event/'+event_key+'/teams/simple?X-TBA-Auth-Key='+api_key)

class ScoutingAPI:
    def __init__(self, event_key, team_key):
        self.event_key = []
        self.team_key = team_key
        if 'events' in event_key:
            events = requests.get('https://www.thebluealliance.com/api/v3/team/frc'+team_key+'/events/2024/simple?X-TBA-Auth-Key='+api_key)
            print(events.json())
            for event in events.json():
                self.event_key.append(event.get("key"))
        else:
            self.event_key = event_key
        print(event_key)
        print(self.event_key)

    def get_start_red(self):
        data = []

        for key in self.event_key:
            r = requests.get('http://team1710scouting.vercel.app/api/'+key+'/frc'+self.team_key)
            for e in r.json():
                data.append(e)

        # with open('data.json', 'r') as f:
        #     data = json.load(f)

        starts = []

        for e in data:
            if e['alliance'] == 'red':
                strat_label = 0
                auto_actions = False
                if e['game']['untimed']['exitAuto']:
                    strat_label += 1
                    for d in e['game']['actions']:
                        if d.get('phase') == 'auto':
                            auto_actions = True
                    if auto_actions:
                        strat_label += 1
                starts.append({'x': e['pregame']['startPosition']['x'], 'y': e['pregame']['startPosition']['y'], 'strat': strat_label})

        print(starts)

        for p in starts:
            x = p.get('x')
            if x > 50:
                p['x'] = 50 - (x - 50)
            elif x < 50:
                p['x'] = 50 + (50 - x)
            elif x == 50:
                p['x'] = 50

        return starts

    def get_start_blue(self):
        data = []

        for key in self.event_key:
            r = requests.get('http://team1710scouting.vercel.app/api/'+key+'/frc'+self.team_key)
            for e in r.json():
                data.append(e)

        # with open('data.json', 'r') as f:
        #     data = json.load(f)

        starts = []

        for e in data:
            if e['alliance'] == 'blue':
                strat_label = 0
                auto_actions = False
                if e['game']['untimed']['exitAuto']:
                    strat_label += 1
                    for d in e['game']['actions']:
                        if d.get('phase') == 'auto':
                            auto_actions = True
                    if auto_actions:
                        strat_label += 1
                starts.append({'x': e['pregame']['startPosition']['x'], 'y': e['pregame']['startPosition']['y'], 'strat': strat_label})

        print(starts)

        return starts