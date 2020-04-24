from pathlib import Path

from model.actions import EndRound
from processors import actionrandomizer
import csv


class Collector:

    def __init__(self):
        self.previous_city = {}
        self.previous_action = {}

    def collect(self, game_round):
        if self.previous_city:
            current_city = next((city for city in game_round.cities if
                                 city.name == self.previous_city.name), None)

            if current_city.score + 0.3 < self.previous_city.score:
                if not isinstance(self.previous_action, EndRound):
                    save_asset(self.previous_city, self.previous_action)

        top_city = sorted(game_round.cities, key=lambda city: city.score, reverse=True).pop(1)
        self.previous_city = top_city
        self.previous_action = actionrandomizer.next_action(top_city, game_round)
        return self.previous_action


def save_asset(city, action):
    path = str(Path(__file__).parent.absolute().parent.absolute().parent.absolute()) + '/models/'

    if not Path(path + 'data.csv').is_file():
        with open(path + 'data.csv', 'w', ) as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['hygiene', 'awareness', 'government', 'economy',
                             'action', 'population', 'connections'])

    with open(path + 'data.csv', 'a', ) as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([city.hygiene, city.awareness, city.government, city.economy,
                         action.getLabel(), city.population, len(city.connections)])
