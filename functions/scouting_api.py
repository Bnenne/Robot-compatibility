import requests, os, pickle
from dotenv import load_dotenv
from functools import wraps
from datetime import datetime, timezone, timedelta
import httpx

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

        if 'events' in event_key: # Check if the event_key is 'events' to get all events
            events = api_call('https://www.thebluealliance.com/api/v3/team/'+self.team_key+'/events/2025/simple?X-TBA-Auth-Key='+self.api_key)
            print(events)
            for event in events:
                self.event_key.append(event.get("key"))
        else:  # If a specific event key is provided
            self.event_key.append(event_key)

        self.data = []

        for key in self.event_key: # Loop through each event key
            print('http://scouting.team1710.com/api/'+key+'/'+self.team_key)
            r = api_call('http://scouting.team1710.com/api/'+key+'/'+self.team_key)
            if r is not None: # Check if the response is not None, been having issues with NoneType responses
                for e in r:
                    self.data.append(e)

    def starts(self):
        """Processes the data to extract starting positions and auto scores

        Returns:
            list: A list of dictionaries containing the starting positions and auto scores for each match
        """
        starts = []

        print('starts data', self.data)

        for e in self.data: # Iterate through each match data
            auto_actions = []
            auto_score = 0
            intake_locations = {
                'processor': 0,
                'coral_station': 0,
                'reef': 0,
                'alliance': 0,
                'barge': 0
            }
            for d in e['actions']: # Iterate through each action in the match
                if d.get('phase') == 'auto':
                    auto_actions.append(d)
            for a in auto_actions: # Process only auto actions
                if a.get('action') == 'score': # Count the auto score
                    auto_score += 1
                if a.get('action') == 'intake': # Count the intakes based on location
                    if a.get('location') is 'coral_station_left' or 'coral_station_right':
                        intake_locations['coral_station'] += 1
                    else:
                        intake_locations[a.get('location')] += 1
            starts.append( # Create a dictionary for each match with the starting position and auto score
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
        try: # Attempt to load the cached data from the pickle file
            cached = pickle.load(open("cache.p", "rb")) # Load the cached data from the pickle file
            current_utc_time = datetime.now(timezone.utc)
            if current_utc_time >= cached[str(*args)]["timestamp"] + timedelta(minutes=10): # Check if the cached data is older than 10 minutes
                result = func(*args, **kwargs) # Call the original function to get fresh data
                cached[str(*args)] = {"data": result, "timestamp": datetime.now(timezone.utc)} # Update the cache with the new result and timestamp
                try: # Attempt to save the updated cache back to the pickle file
                    pickle.dump(cached, open("cache.p", "wb"))
                except: # If there's an error saving, ensure the file is opened correctly
                    with open("cache.p", "wb") as f:
                        pickle.dump(cached, f)
                    return result
            else: # If the cached data is still valid (not older than 10 minutes)
                return cached[str(*args)]["data"]
        except: # If the cache file does not exist or is corrupted, create a new cache
            result = func(*args, **kwargs) # Call the original function to get fresh data
            try: # Attempt to create a new cache file or load existing cache
                cached = pickle.load(open("cache.p", "rb"))
                cached[str(*args)] = {"data": result, "timestamp": datetime.now(timezone.utc)}
            except: # If the cache file does not exist or is corrupted, create a new cache
                cached = {str(*args): {"data": result, "timestamp": datetime.now(timezone.utc)}}
            try: # Attempt to save the updated cache back to the pickle file
                pickle.dump(cached, open("cache.p", "wb"))
            except: # If there's an error saving, ensure the file is opened correctly
                with open("cache.p", "wb") as f:
                    pickle.dump(cached, f)
            return result
    return wrapper

@cache # Cache the data to avoid frequent API calls and speed up the response time
async def api_call(url):
    """Makes an API call to the given URL and returns the JSON response

    Args:
        url (str): The URL to make the API call to
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    return response.json() if response.status_code == 200 else None