import requests

class scoutingAPI:
    def __init__(self, event_keys, team_key):
        self.event_keys = event_keys
        self.team_key = team_key

    def auto_strat(self, positions):
        data = []

        for key in self.event_keys:
            r = requests.get('http://team1710scouting.vercel.app/api/'+key+'/frc'+self.team_key)
            for e in r.json():
                data.append(e)

        strat = []

        for p in positions:
            for d in data:
                if p == d['pregame']['startPosition']:
                    if d['game']['untimed']['exitAuto'] == True:
                        strat.append({'x': p.get('x'), 'y': p.get('y'), 'strat': 1})
                    else:
                        strat.append({'x': p.get('x'), 'y': p.get('y'), 'strat': 0})

        return(strat)

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

        return(self.auto_strat(starts))

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

        return(self.auto_strat(starts))