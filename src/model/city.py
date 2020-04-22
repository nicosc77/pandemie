from processors.eventprocessor import process_event


class City:

    def __init__(self, data):
        self.name = data['name']
        self.population = data['population']

        self.connections = []
        for connection in data['connections']:
            self.connections.append(connection)

        self.hygiene = data['hygiene']
        self.government = data['government']
        self.awareness = data['awareness']
        self.economy = data['economy']
        self.score = int
        self.effective_action = {}

        self.events = []
        try:
            for event in data['events']:
                self.events.append(process_event(event))
        except KeyError:
            pass

    def __str__(self):
        return self.name + ' awa ' + self.awareness + ' sco ' + str(self.score) + ' eco ' + \
               self.economy + ' gov ' + self.government + ' hyg ' + self.hygiene