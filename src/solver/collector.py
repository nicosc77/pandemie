from pathlib import Path

from model.actions import EndRound
from processors.actionrandomizer import get_next_action
import csv


class Collector:

    def __init__(self):
        self.previous_city = {}
        self.previous_action = {}

    def collect(self, game_round):
        if self.previous_city:
            current_city = self.get_new_stats()

            if current_city.score + 0.3 < self.previous_city.score:
                if not isinstance(self.previous_action, EndRound):
                    self.save_asset()

        top_city = get_top_city(game_round)
        self.previous_city = top_city
        self.previous_action = get_next_action(top_city, game_round)
        return self.previous_action

    def get_new_stats(self):
        return next((city for city in game_round.cities if city.name == self.previous_city.name), None)

    def save_asset(self):
        path = str(Path(__file__).parent.absolute().parent.absolute().parent.absolute()) + '/models/'

        if not Path(path + 'data.csv').is_file():
            with open(path + 'data.csv', 'w', ) as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(['hygiene', 'awareness', 'government', 'economy',
                                 'action', 'population', 'connections'])

        with open(path + 'data.csv', 'a', ) as csv_file:
            writer = csv.writer(csv_file)
            city = self.previous_city
            action = self.previous_action
            writer.writerow([city.hygiene, city.awareness, city.government, city.economy,
                             action.getLabel(), city.population, len(city.connections)])