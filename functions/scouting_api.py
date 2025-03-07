import requests, os, json
from dotenv import load_dotenv

class ScoutingAPI:
    def __init__(self, event_key, team_key):
        self.event_key = []
        self.team_key = team_key
        load_dotenv()
        self.api_key = os.getenv("API_KEY")
        if 'events' in event_key:
            events = requests.get('https://www.thebluealliance.com/api/v3/team/'+self.team_key+'/events/2025/simple?X-TBA-Auth-Key='+self.api_key)
            print('events.json()', events.json())
            for event in events.json():
                self.event_key.append(event.get("key"))
        else:
            self.event_key.append(event_key)

        self.data = []

        for key in self.event_key:
            r = requests.get('http://scouting.team1710.com/api/'+key+'/'+self.team_key)
            for e in r.json():
                self.data.append(e)

        # self.data = []
        # self.team_key = team_key

    def get_start_red(self):
        # with open(str(self.team_key)+'.json', 'r') as f:
        #     self.data = json.load(f)

        starts = self.starts('red', self.data)

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
        # with open(str(self.team_key)+'.json', 'r') as f:
        #     self.data = json.load(f)

        starts = self.starts('blue', self.data)

        return starts

    def starts(self, color, data):
        starts = []

        for e in data:
            auto_actions = []
            auto_score = 0
            intake_locations = {
                'amp': 0,
                'speaker': 0,
                'trap': 0,
                'center': 0
            }
            if e['alliance'] == color:
                for d in e['game']['actions']:
                    if d.get('phase') == 'auto':
                        auto_actions.append(d)
                for a in auto_actions:
                    if a.get('action') == 'score':
                        auto_score += 1
                    if a.get('action') == 'intake':
                        if a.get('location') == 'amp':
                            intake_locations['amp'] += 1
                        if a.get('location') == 'speaker':
                            intake_locations['speaker'] += 1
                        if a.get('location') == 'trap':
                            intake_locations['trap'] += 1
                        if a.get('location') == 'center':
                            intake_locations['center'] += 1
                starts.append(
                    {
                    'x': e['pregame']['startPosition']['x'],
                    'y': e['pregame']['startPosition']['y'],
                    'auto_score': auto_score,
                    'team': e['team'],
                    'amp': intake_locations['amp'],
                    'speaker': intake_locations['speaker'],
                    'trap': intake_locations['trap'],
                    'center': intake_locations['center'],
                    }
                )

        print('starts', starts)
        return starts

    def get_tele_actions(self):
        # with open(str(self.team_key)+'.json', 'r') as f:
        #     self.data = json.load(f)

        actions = []

        for d in self.data:
            for e in d['game']['actions']:
                if e['phase'] == 'teleOp':
                    actions.append(e)

        return actions

def return_scoutingapi():
    events = requests.get('http://scouting.team1710.com/api/key/event')
    teams = requests.get('http://scouting.team1710.com/api/key/team')
    return {'events': events.json(), 'teams': teams.json()}

def return_tba():
    load_dotenv()
    api_key = os.getenv("API_KEY")
    data = requests.get('https://www.thebluealliance.com/api/v3/events/2025/simple?X-TBA-Auth-Key='+api_key)
    return data.json()

def return_teams(event):
    load_dotenv()
    api_key = os.getenv("API_KEY")
    data = requests.get('https://www.thebluealliance.com/api/v3/event/'+event+'/teams/simple?X-TBA-Auth-Key=' + api_key)
    return data.json()