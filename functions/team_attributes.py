from schema import attribute_schema
from starting_clusters import StartingClusters

class TeamAttributes:
    def __init__(self, team):
        self.team = team
        self.attributes = attribute_schema
        self.attributes["starting_clusters"] = StartingClusters()

    def place(self, phase, action, location):
        match_stats = self.attributes["phases"][phase]["place"]

        if type(location) is int:
            match_stats["reef"][action] += 1

            match location:
                case 1:
                    match_stats["l1"][action] += 1

                case 2:
                    match_stats["l2"][action] += 1

                case 3:
                    match_stats["l3"][action] += 1

                case 4:
                    match_stats["l4"][action] += 1
        else:
            match_stats[location][action] += 1

    def algae_remove(self, phase):
        self.attributes["phases"][phase]["algae_remover"] = 1

    def climb(self, climb):
        match climb:
            case "none":
                pass

            case "deep":
                self.attributes["deep_hang"] = 1
                self.attributes["no_hang"] = -1

            case "shallow":
                self.attributes["shallow_hang"] = 1
                self.attributes["no_hang"] = -1

    def leave(self, left_start):
        if left_start:
            self.attributes['auto_leave'] = 1

    def update(self):
        for phase in self.attributes["phases"]:
            total = 0

            for location in self.attributes["phases"][phase]["place"]:
                stats = self.attributes["phases"][phase]["place"][location]
                total += stats["score"] + stats["miss"]

            for location in self.attributes["phases"][phase]["place"]:
                stats = self.attributes["phases"][phase]["place"][location]
                location_total = stats["score"] + stats["miss"]

                if stats["score"] == 0:
                    stats["accuracy"] = 0
                else:
                    stats["accuracy"] = stats["score"]  / location_total

                if location_total == 0:
                    stats["frequency"] = 0
                else:
                    stats["ability"] = 1
                    stats["frequency"] = location_total  / total

    def add_starting_position(self, x, y):
        self.attributes["starting_clusters"].starting_positions.append((x, y))