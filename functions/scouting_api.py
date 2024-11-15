import requests, os
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

    def auto_strat(self, positions, data):

        strat = []

        for p in positions:
            stratLabel = 0
            autoActions = False
            for d in data:
                if p == d['pregame']['startPosition']:
                    if d['game']['untimed']['exitAuto']:
                        stratLabel += 1
                        for e in d['game']['actions']:
                            if e.get('phase') == 'auto':
                                autoActions = True
                        if autoActions:
                            stratLabel += 1
            strat.append({'x': p.get('x'), 'y': p.get('y'), 'strat': stratLabel})

        return strat

    def get_start_red(self):
        data = []
            
        for key in self.event_key:
            r = requests.get('http://team1710scouting.vercel.app/api/'+key+'/frc'+self.team_key)
            for e in r.json():
                data.append(e)

        starts = []

        for e in data:
            if e['alliance'] == 'red':
                starts.append(e['pregame']['startPosition'])

        for p in starts:
            x = p.get('x')
            if x > 50:
                p['x'] = 50 - (x - 50)
            elif x < 50:
                p['x'] = 50 + (50 - x)
            elif x == 50:
                p['x'] = 50

        return self.auto_strat(starts, data)
        # return starts

    def get_start_blue(self):
        data = []

        for key in self.event_key:
            r = requests.get('http://team1710scouting.vercel.app/api/'+key+'/frc'+self.team_key)
            for e in r.json():
                data.append(e)

        starts = []

        for e in data:
            if e['alliance'] == 'blue':
                starts.append(e['pregame']['startPosition'])

        return self.auto_strat(starts, data)
        # return starts


# def get_start_red(event_keys, team_key):
#
#     data = []
#
#     for key in event_keys:
#         r = requests.get('http://team1710scouting.vercel.app/api/'+key+'/frc'+team_key)
#         for e in r.json():
#             data.append(e)
#
#     starts = []
#
#     for e in data:
#         if e['alliance'] == 'red':
#             starts.append(e['pregame']['startPosition'])
#     print(starts)
#     for p in starts:
#         x = p.get('x')
#         if x > 50:
#             p['x'] = 50 - (x - 50)
#         elif x < 50:
#             p['x'] = 50 + (50 - x)
#         elif x == 50:
#             p['x'] = 50
#     print(starts)
#     return starts
#
# def get_start_blue(event_keys, team_key):
#     import requests
#
#     data = []
#
#     for key in event_keys:
#         r = requests.get('http://team1710scouting.vercel.app/api/'+key+'/frc'+team_key)
#         for e in r.json():
#             data.append(e)
#
#     starts = []
#
#     for e in data:
#         if e['alliance'] == 'blue':
#             starts.append(e['pregame']['startPosition'])
#
#     return starts