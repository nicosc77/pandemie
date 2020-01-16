from model.city import City
from processors.eventprocessor import process_event


class GameRound:

    def __init__(self, data):
        self.outcome = data['outcome']
        self.round = data['round']
        self.points = data['points']
        self.cities = []

        for city, value in data['cities'].items():
            self.cities.append(City(value))

        self.events = []
        try:
            for event in data['events']:
                self.events.append(process_event(event))
        except KeyError:
            pass

        try:
            self.error = data['error']
        except KeyError:
            pass
