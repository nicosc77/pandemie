from model.events import Outbreak, BioTerrorrism, MedicationDeployed, \
    VaccineDeployed, AntiVaccinationism, LargeScalePanic, Quarantine, \
    EconomicCrisis, ConnectionClosed, \
    AirportClosed, Uprising


def score(game_round):
    for city in game_round.cities:
        city.score = process_city(city, game_round.events)
    return sortCities(game_round)


def sortCities(game_round):
    game_round.cities = sorted(game_round.cities, key=lambda city: city.score,
                               reverse=True)
    return game_round


def process_city(city, global_events):
    hygiene = parse_letter(city.hygiene, 1.15)
    awareness = parse_letter(city.awareness, 1.092)
    economy = parse_letter(city.economy, 0.72)
    government = parse_letter(city.government, 0.8525)

    if len(city.connections) == 9:
        connections = 1
    elif len(city.connections) == 8:
        connections = 0.9
    elif len(city.connections) == 7:
        connections = 0.8
    elif len(city.connections) == 6:
        connections = 0.7
    elif len(city.connections) == 5:
        connections = 0.6
    elif len(city.connections) == 4:
        connections = 0.5
    elif len(city.connections) == 3:
        connections = 0.4
    elif len(city.connections) == 2:
        connections = 0.3
    elif len(city.connections) == 1:
        connections = 0.2
    elif len(city.connections) == 0:
        connections = 0.1
    else:
        connections = 0.1

    if city.population > 10000:
        population = 1
    elif city.population < 10000:
        population = 0.9
    elif city.population < 8000:
        population = 0.8
    elif city.population < 6000:
        population = 0.7
    elif city.population < 5000:
        population = 0.6
    elif city.population < 4000:
        population = 0.5
    elif city.population < 3000:
        population = 0.4
    elif city.population < 2000:
        population = 0.3
    elif city.population < 1000:
        population = 0.2
    else:
        population = 0.1

    pathogen = 0

    for x in city.events:
        if isinstance(x, Outbreak):
            pathogen += (parse_letter(x.pathogen.infectivity) + parse_letter(
                x.pathogen.mobility) + parse_letter(
                x.pathogen.duration) + parse_letter(
                x.pathogen.lethality)) * x.prevalence * population
        if isinstance(x, BioTerrorrism):
            pathogen += parse_letter(x.pathogen.infectivity) + parse_letter(
                x.pathogen.mobility) + parse_letter(
                x.pathogen.duration) + parse_letter(
                x.pathogen.lethality) * population
        if isinstance(x, Uprising):
            government = government * 2 * (x.participants / city.population)
        if isinstance(x, AirportClosed):
            connections = connections * 0.2
        if isinstance(x, ConnectionClosed):
            connections = connections * 0.7
        if isinstance(x, AntiVaccinationism):
            awareness = awareness * 5 * population
        if isinstance(x, EconomicCrisis):
            economy = economy * 3
        if isinstance(x, Quarantine):
            pathogen = 0
            connections = 0
        if isinstance(x, LargeScalePanic):
            economy = economy * 2 * population
            government = government * 1.5 * population
        if isinstance(x, VaccineDeployed):
            pathogen = pathogen * 0.7
        if isinstance(x, MedicationDeployed):
            pathogen = pathogen * 0.8

    scores = [hygiene * 1.15, economy * 1.15, awareness * 1.15, government * 1.15, connections,
              population * 1.5, pathogen * 2]

    return sum(scores)


def parse_letter(letter: str, multplicator: float = 1) -> float:
    output = 1
    if letter == '++':
        output = 0
    elif letter == '+':
        output = 0.25
    elif letter == 'o':
        output = 0.5
    elif letter == '-':
        output = 0.75
    elif letter == '--':
        output = 1
    return output * multplicator
