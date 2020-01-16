from model.pathogen import Pathogen


class AirportClosed:

    def __init__(self, data):
        self.type = data['type']
        self.since_round = data['sinceRound']
        self.until_round = data['untilRound']


class AntiVaccinationism:

    def __init__(self, data):
        self.type = data['type']
        self.since_round = data['sinceRound']


class BioTerrorrism:

    def __init__(self, data):
        self.type = data['type']
        self.round = data['round']
        self.pathogen = Pathogen(data['pathogen'])


class CampaignLaunched:

    def __init__(self, data):
        self.type = data['type']
        self.round = data['round']


class ConnectionClosed:

    def __init__(self, data):
        self.type = data['type']
        self.city = data['city']
        self.since_round = data['sinceRound']
        self.until_round = data['untilRound']


class EconomicCrisis:

    def __init__(self, data):
        self.type = data['type']
        self.since_round = data['sinceRound']


class ElectionsCalled:

    def __init__(self, data):
        self.type = data['type']
        self.round = data['round']


class HygienicMeasuresApplied:

    def __init__(self, data):
        self.type = data['type']
        self.round = data['round']


class InfluenceExcerted:

    def __init__(self, data):
        self.type = data['type']
        self.round = data['round']


class LargeScalePanic:

    def __init__(self, data):
        self.type = data['type']
        self.since_round = data['sinceRound']


class MedicationAvailable:

    def __init__(self, data):
        self.type = data['type']
        self.pathogen = Pathogen(data['pathogen'])
        self.since_round = data['sinceRound']


class MedicationDeployed:

    def __init__(self, data):
        self.type = data['type']
        self.pathogen = Pathogen(data['pathogen'])
        self.round = data['round']


class MedicationInDevelopment:

    def __init__(self, data):
        self.type = data['type']
        self.pathogen = Pathogen(data['pathogen'])
        self.since_round = data['sinceRound']
        self.until_round = data['untilRound']


class Outbreak:

    def __init__(self, data):
        self.type = data['type']
        self.pathogen = Pathogen(data['pathogen'])
        self.since_round = data['sinceRound']
        self.prevalence = data['prevalence']


class PathogenEncountered:

    def __init__(self, data):
        self.type = data['type']
        self.pathogen = Pathogen(data['pathogen'])
        self.round = data['round']


class Quarantine:

    def __init__(self, data):
        self.type = data['type']
        self.since_round = data['sinceRound']
        self.until_round = data['untilRound']


class Uprising:

    def __init__(self, data):
        self.type = data['type']
        self.since_round = data['sinceRound']
        self.participants = data['participants']


class VaccineAvailable:

    def __init__(self, data):
        self.type = data['type']
        self.pathogen = Pathogen(data['pathogen'])
        self.since_round = data['sinceRound']


class VaccineDeployed:

    def __init__(self, data):
        self.type = data['type']
        self.pathogen = Pathogen(data['pathogen'])
        self.round = data['round']


class VaccineInDevelopment:

    def __init__(self, data):
        self.type = data['type']
        self.pathogen = Pathogen(data['pathogen'])
        self.since_round = data['sinceRound']
        self.until_round = data['untilRound']
