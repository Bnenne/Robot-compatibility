import requests, os, pickle
from dotenv import load_dotenv
from functools import wraps
from datetime import datetime, timezone, timedelta

class ScoutingAPI:
    def __init__(self, event_key, team_key):
        """Initializes the ScoutingAPI class with the given event key and team key

        Args:
            event_key (str): The event key (e.g., '2025cttd') or 'events' for all events
            team_key (str): The team key (e.g., 'frc1710')
        """
        self.event_key = []
        self.team_key = team_key
        load_dotenv()
        self.api_key = os.getenv("API_KEY")
        if 'events' in event_key:
            events = api_call('https://www.thebluealliance.com/api/v3/team/'+self.team_key+'/events/2025/simple?X-TBA-Auth-Key='+self.api_key)
            print(events)
            for event in events:
                self.event_key.append(event.get("key"))
        else:
            self.event_key.append(event_key)

        self.data = []

        for key in self.event_key:
            print('http://scouting.team1710.com/api/'+key+'/'+self.team_key)
            r = api_call('http://scouting.team1710.com/api/'+key+'/'+self.team_key)
            if r is not None:
                for e in r:
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

    def get_starts(self):
        """Retrieves the starting positions and auto scores for the team

        Returns:
            list: A list of dictionaries containing the starting positions and auto scores for each match
        """
        # with open(str(self.team_key)+'.json', 'r') as f:
        #     self.data = json.load(f)

        starts = self.starts(self.data)

        return starts

    def starts(self, data):
        """Processes the data to extract starting positions and auto scores

        Args:
            data (list): The list of match data for the team

        Returns:
            list: A list of dictionaries containing the starting positions and auto scores for each match
        """
        starts = []

        print('starts data', data)

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
                'x': 0,
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

        print('starts', starts)
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

def cache(func):
    """A decorator to cache the results of a function for 10 minutes using pickle

    Args:
        func (function): The function to be cached
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            cached = pickle.load(open("cache.p", "rb"))
            current_utc_time = datetime.now(timezone.utc)
            if current_utc_time >= cached[str(*args)]["timestamp"] + timedelta(minutes=10):
                result = func(*args, **kwargs)
                cached[str(*args)] = {"data": result, "timestamp": datetime.now(timezone.utc)}
                try:
                    pickle.dump(cached, open("cache.p", "wb"))
                except:
                    with open("cache.p", "wb") as f:
                        pickle.dump(cached, f)
                    return result
            else:
                return cached[str(*args)]["data"]
        except:
            result = func(*args, **kwargs)
            try:
                cached = pickle.load(open("cache.p", "rb"))
                cached[str(*args)] = {"data": result, "timestamp": datetime.now(timezone.utc)}
            except:
                cached = {str(*args): {"data": result, "timestamp": datetime.now(timezone.utc)}}
            try:
                pickle.dump(cached, open("cache.p", "wb"))
            except:
                with open("cache.p", "wb") as f:
                    pickle.dump(cached, f)
            return result
    return wrapper

@cache
def api_call(url):
    """Makes an API call to the given URL and returns the JSON response

    Args:
        url (str): The URL to make the API call to
    """
    response = requests.get(url)
    return response.json() if response.status_code == 200 else None