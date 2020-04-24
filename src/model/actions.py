class ApplyHygienicMesaures:

    def __init__(self, city=None):
        if city is not None:
            self.city = city.name

    def getMessage(self):
        return '{"type":"applyHygienicMeasures", "city":"' + str(
            self.city) + '"}'

    @staticmethod
    def getLabel():
        return 'applyHygienicMeasures'

    @staticmethod
    def getPoints():
        return 3


class CallElections:

    def __init__(self, city=None):
        if city is not None:
            self.city = city.name

    def getMessage(self):
        return '{"type":"callElections", "city":"' + str(self.city) + '"}'

    @staticmethod
    def getLabel():
        return "callElections"

    @staticmethod
    def getPoints():
        return 3


class CloseAirport:

    def __init__(self, city=None, rounds=None):
        if city is not None:
            self.city = city.name
            self.rounds = rounds

    @staticmethod
    def getLabel():
        return "closeAirport"

    def getMessage(self):
        return '{"type":"closeAirport", "city": "' + str(
            self.city) + '", "rounds": ' + str(self.rounds) + '}'

    def getPoints(self):
        return 5 * self.rounds + 15

    @staticmethod
    def calculateRounds(points):
        rounds = round((points - 15) / 5) - 1
        if rounds < 1:
            return 1
        elif rounds > 5:
            return 5
        else:
            return rounds


class CloseConnection:

    def __init__(self, source=None, destination=None, rounds=None):
        if source is not None:
            self.source = source.name
            self.destination = destination
            self.rounds = rounds

    @staticmethod
    def getLabel():
        return "closeConnection"

    def getMessage(self):
        return '{"type":"closeConnection", "fromCity": "' + str(
            self.source) + '", "toCity": "' + str(self.destination) \
            + '", "rounds": ' + str(self.rounds) + '}'

    def getPoints(self):
        return 3 * self.rounds + 3

    @staticmethod
    def calculateRounds(points):
        rounds = round((points - 3) / 3) - 1
        if rounds <= 1:
            return 1
        elif rounds > 5:
            return 5
        else:
            return rounds


class DeployMedication:

    def __init__(self, city=None, pathogen=None):
        if city is not None:
            self.city = city.name
            self.pathogen = pathogen

    @staticmethod
    def getLabel():
        return "medication"

    def getMessage(self):
        return '{"type":"deployMedication", "pathogen":"' + str(
            self.pathogen.name) + '", "city":"' + str(
            self.city) + '"}'

    @staticmethod
    def getPoints():
        return 10


class DeployVaccine:

    def __init__(self, city=None, pathogen=None):
        if city is not None:
            self.city = city.name
            self.pathogen = pathogen

    @staticmethod
    def getLabel():
        return "vaccine"

    def getMessage(self):
        return '{"type":"deployVaccine", "pathogen":"' + str(
            self.pathogen.name) + '", "city":"' + str(self.city) + '"}'

    @staticmethod
    def getPoints():
        return 5


class DevelopMedication:

    def __init__(self, pathogen=None):
        if pathogen is not None:
            self.pathogen = pathogen

    @staticmethod
    def getLabel():
        return "medication"

    def getMessage(self):
        return '{"type":"developMedication", "pathogen":"' + str(
            self.pathogen.name) + '"}'

    @staticmethod
    def getPoints():
        return 20


class DevelopVaccine:

    def __init__(self, pathogen=None):
        if pathogen is not None:
            self.pathogen = pathogen

    @staticmethod
    def getLabel():
        return "vaccine"

    def getMessage(self):
        return '{"type":"developVaccine", "pathogen":"' + str(
            self.pathogen.name) + '"}'

    @staticmethod
    def getPoints():
        return 40


class EndRound:

    @staticmethod
    def getMessage():
        return '{"type":"endRound"}'

    @staticmethod
    def getLabel():
        return "endRound"

    @staticmethod
    def getPoints():
        return 0


class ExertInfluence:

    def __init__(self, city=None):
        if city is not None:
            self.city = city.name

    def getMessage(self):
        return '{"type":"exertInfluence", "city":"' + str(self.city) + '"}'

    @staticmethod
    def getLabel():
        return "exertInfluence"

    @staticmethod
    def getPoints():
        return 3


class LaunchCampaign:

    def __init__(self, city=None):
        if city is not None:
            self.city = city.name

    def getMessage(self):
        return '{"type":"launchCampaign", "city":"' + str(self.city) + '"}'

    @staticmethod
    def getLabel():
        return "launchCampaign"

    @staticmethod
    def getPoints():
        return 3


class PutUnderQuarantine:

    def __init__(self, city=None, rounds=None):
        if city is not None:
            self.city = city.name
            self.rounds = rounds

    @staticmethod
    def getLabel():
        return "putUnderQuarantine"

    def getMessage(self):
        return '{"type":"putUnderQuarantine", "city": "' + str(
            self.city) + '", "rounds": ' + str(self.rounds) + '}'

    def getPoints(self):
        return 10 * self.rounds + 20

    @staticmethod
    def calculateRounds(points):
        rounds = round((points - 20) / 10) - 1
        if rounds <= 1:
            return 1
        elif rounds > 5:
            return 5
        else:
            return rounds
