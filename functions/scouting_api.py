import requests

class ScoutingAPI:
    def __init__(self, event_keys, team_key):
        self.event_keys = event_keys
        self.team_key = team_key

    def auto_strat(self, positions, data):

        strat = []

        for p in positions:
            for d in data:
                if p == d['pregame']['startPosition']:
                    if d['game']['untimed']['exitAuto']:
                        strat.append({'x': p.get('x'), 'y': p.get('y'), 'strat': 2})
                    else:
                        strat.append({'x': p.get('x'), 'y': p.get('y'), 'strat': 1})

        return strat

    def get_start_red(self):
        data = []

        for key in self.event_keys:
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

        for key in self.event_keys:
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