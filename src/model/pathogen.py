class Pathogen:

    def __init__(self, data):
        self.name = data['name']
        self.infectivity = data['infectivity']
        self.mobility = data['mobility']
        self.duration = data['duration']
        self.lethality = data['lethality']
