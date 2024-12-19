from functions.scouting_api import ScoutingAPI

class StrategyLabeling:
    def __init__(self, event_key, team_key):
        self.event_key = event_key
        self.team_key = team_key
        sa = ScoutingAPI(self.event_key, self.team_key)

        self.data = sa.get_tele_actions()

    def tele_actions(self):
        intakes = [
            {"location": "amp", "intakes": 0},
            {"location": "center", "intakes": 0},
            {"location": "speaker", "intakes": 0},
            {"location": "source", "intakes": 0},
            {"location": "trap", "intakes": 0}
        ]
        scores = [
            {"location": "speaker", "scores": 0},
            {"location": "amp", "scores": 0},
            {"location": "trap", "scores": 0}
        ]
        misses = [
            {"location": "amp", "misses": 0},
            {"location": "center", "misses": 0},
            {"location": "speaker", "misses": 0},
            {"location": "source", "misses": 0},
            {"location": "trap", "misses": 0}
        ]

        for d in self.data:
            if d['action'] == 'intake':
                for intake in intakes:
                    if intake['location'] == d['location']:
                        intake['intakes'] += 1
            if d['action'] == 'score':
                for score in scores:
                    if score['location'] == d['location']:
                        score['scores'] += 1
            if d['action'] == 'miss':
                for miss in misses:
                    if miss['location'] == d['location']:
                        miss['misses'] += 1

        return {"intakes": intakes, "scores": scores, "misses": misses}