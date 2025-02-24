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
            print(events.json())
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
        # self.team_key = team_key[3:]
        #
        # with open('data.json', 'r') as f:
        #     file_data = json.load(f)
        #
        # for f in file_data:
        #     if f['team'] == self.team_key:
        #         self.data.append(f)

    def get_start_red(self):
        # with open(str(self.team_key)+'.json', 'r') as f:
        #     self.data = json.load(f)

        starts = self.starts('red', self.data)

        # for p in starts:
        #     x = p.get('x')
        #     if x > 50:
        #         p['x'] = 50 - (x - 50)
        #     elif x < 50:
        #         p['x'] = 50 + (50 - x)
        #     elif x == 50:
        #         p['x'] = 50

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
                'processor': 0,
                'coral_station': 0,
                'reef': 0,
                'alliance': 0,
                'barge': 0
            }
            if e['alliance'] == color:
                for d in e['actions']:
                    if d.get('phase') == 'auto':
                        auto_actions.append(d)
                for a in auto_actions:
                    if a.get('action') == 'score':
                        auto_score += 1
                    if a.get('action') == 'intake':
                        if a.get('location') == 'processor':
                            intake_locations['processor'] += 1
                        if a.get('location') == 'coral_station':
                            intake_locations['coral_station'] += 1
                        if a.get('location') == 'reef':
                            intake_locations['reef'] += 1
                        if a.get('location') == 'alliance':
                            intake_locations['alliance'] += 1
                        if a.get('location') == 'barge':
                            intake_locations['barge'] += 1
                starts.append(
                    {
                    'x': e['pregame']['startPosition']['x'],
                    'y': e['pregame']['startPosition']['y'],
                    'auto_score': auto_score,
                    'team': e['team'],
                    'processor': intake_locations['processor'],
                    'coral_station': intake_locations['coral_station'],
                    'reef': intake_locations['reef'],
                    'alliance': intake_locations['alliance'],
                    'barge': intake_locations['barge']
                    }
                )

        print(starts)
        return starts

    def get_tele_actions(self):
        # with open(str(self.team_key)+'.json', 'r') as f:
        #     self.data = json.load(f)

        actions = []

        for d in self.data:
            for e in d['actions']:
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