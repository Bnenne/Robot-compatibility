def get_start_red(event_keys, team_key):
    import requests

    data = []

    for key in event_keys:
        r = requests.get('http://team1710scouting.vercel.app/api/'+key+'/frc'+team_key)
        for e in r.json():
            data.append(e)

    starts = []

    for e in data:
        if e['alliance'] == 'red':
            starts.append(e['pregame']['startPosition'])

    return(starts)

def get_start_blue(event_keys, team_key):
    import requests

    data = []

    for key in event_keys:
        r = requests.get('http://team1710scouting.vercel.app/api/'+key+'/frc'+team_key)
        for e in r.json():
            data.append(e)

    starts = []

    for e in data:
        if e['alliance'] == 'blue':
            starts.append(e['pregame']['startPosition'])

    return(starts)