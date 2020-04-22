import numpy as np

from model.events import Outbreak, BioTerrorrism, AntiVaccinationism, \
    LargeScalePanic, Quarantine, EconomicCrisis, \
    ConnectionClosed, \
    AirportClosed, Uprising


def process_city(city):
    hygiene = parse_letter(city.hygiene)
    awareness = parse_letter(city.awareness)
    economy = parse_letter(city.economy)
    government = parse_letter(city.government)

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
        if isinstance(x, BioTerrorrism):
            pathogen += parse_letter(x.pathogen.infectivity) + parse_letter(
                x.pathogen.mobility) + parse_letter(
                x.pathogen.duration) + parse_letter(
                x.pathogen.lethality) * population

    array = np.array(
        [hygiene, economy, awareness, government, connections, population,
         pathogen])
    return array


def parse_letter(letter, multplicator=1):
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
