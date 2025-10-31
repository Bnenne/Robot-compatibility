from team_attributes import TeamAttributes
import json

def define_team(team):
    file_path = './data/2025entries.json'
    exclude_events = ['2025cttd']
    team = TeamAttributes(team)

    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    for doc in data:
        if doc["team"] == team.team and doc['event'] not in exclude_events:
            for action in doc['actions']:

                match action['action']:
                    case 'score':
                        if 'level' in action:
                            team.place(action['phase'], 'score', action['level'])
                        else:
                            team.place(action['phase'], 'score', action['location'])

                    case 'miss':
                        if 'level' in action:
                            team.place(action['phase'], 'miss', action['level'])
                        else:
                            team.place(action['phase'], 'miss', action['location'])

                    case 'intake':
                        if action['location'] == 'reef':
                            team.algae_remove(action['phase'])

                    case _:
                        pass

            team.climb(doc['climb']['type'])
            team.leave(doc['untimed']['exitAuto'])
            team.add_starting_position( # Starting position selector dimensions 151x337
                doc['pregame']['startPosition']['x'],
                doc['pregame']['startPosition']['y']
            )

    team.update()

    team.attributes['starting_clusters'].format_data()
    team.attributes['starting_clusters'].cluster()
    team.attributes['starting_clusters'].mass()

    team.attributes['starting_clusters'] = team.attributes['starting_clusters'].clusters

    return team.attributes