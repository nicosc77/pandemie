import random

from model.actions import ApplyHygienicMesaures, CloseAirport, CallElections, \
    DeployMedication, DeployVaccine, \
    DevelopMedication, DevelopVaccine, LaunchCampaign, PutUnderQuarantine, \
    EndRound, ExertInfluence, CloseConnection
from model.events import Quarantine, ConnectionClosed, VaccineInDevelopment, \
    VaccineAvailable, \
    MedicationInDevelopment, MedicationAvailable, Outbreak


def next_action(city, game_round):
    points = game_round.points
    global_events = game_round.events,
    cities = game_round.cities
    rand = random.randint(0, 12)
    rounds = 1

    if rand == 0:
        action = ApplyHygienicMesaures(city)
        if action.getPoints() < points:
            return action
        else:
            return EndRound()

    elif rand == 1:
        action = CallElections(city)
        if action.getPoints() < points:
            return action
        else:
            return EndRound()

    elif rand == 2:
        if any(isinstance(x, Quarantine) for x in city.events):
            pass
        else:
            action = CloseAirport(city, rounds)
            if action.getPoints() < points:
                return action
            else:
                return EndRound()

    elif rand == 3:

        if len(city.connections) != 0:

            already_closed = []
            possible_cities = []

            for x in city.events:
                if isinstance(x, ConnectionClosed):
                    already_closed.append(x.city)

            for y in city.connections:
                if y not in already_closed:
                    for z in cities:
                        if z.name == y:
                            possible_cities.append(z)

            connection = sorted(possible_cities, key=lambda a: a.score,
                                reverse=True).pop(1)

            action = CloseConnection(city, connection.name, rounds)
            if action.getPoints() < points:
                return action
            else:
                return EndRound()

    elif rand == 4:
        action = ExertInfluence(city)
        if action.getPoints() < points:
            return action
        else:
            return EndRound()

    elif rand == 5:
        action = LaunchCampaign(city)
        if action.getPoints() < points:
            return action
        else:
            return EndRound()

    elif rand == 6:
        if any(isinstance(x, Quarantine) for x in city.events):
            pass
        else:
            action = PutUnderQuarantine(city, rounds)
            if action.getPoints() < points:
                return action
            else:
                return EndRound()

    elif rand == 7 or rand == 9 or rand == 11:
        for x in city.events:
            if isinstance(x, Outbreak):
                for y in global_events:
                    if isinstance(y, VaccineInDevelopment):
                        return EndRound()
                    elif isinstance(y, VaccineAvailable):
                        if x.pathogen.name == y.pathogen.name:
                            action = DeployVaccine(city, y.pathogen)
                            if action.getPoints() < points:
                                return action
                            else:
                                return EndRound()

                action = DevelopVaccine(x.pathogen)
                if action.getPoints() < points:
                    return action
                else:
                    return EndRound()

    elif rand == 8 or rand == 10 or rand == 12:
        for x in city.events:
            if isinstance(x, Outbreak):
                for y in global_events:
                    if isinstance(y, MedicationInDevelopment):
                        return EndRound()
                    elif isinstance(y, MedicationAvailable):
                        if x.pathogen.name == y.pathogen.name:
                            action = DeployMedication(city, y.pathogen)
                            if action.getPoints() < points:
                                return action
                            else:
                                return EndRound()

                action = DevelopMedication(x.pathogen)
                if action.getPoints() < points:
                    return action
                else:
                    return EndRound()

    return EndRound()
