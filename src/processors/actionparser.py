import numpy

from model.actions import EndRound, PutUnderQuarantine, LaunchCampaign, ExertInfluence, DevelopVaccine, DeployVaccine, \
    DevelopMedication, DeployMedication, CloseConnection, CloseAirport, CallElections, ApplyHygienicMesaures
from model.events import Quarantine, VaccineInDevelopment, VaccineAvailable, MedicationInDevelopment, \
    MedicationAvailable, Outbreak, ConnectionClosed, AirportClosed

sorted_action_numbers = []


# Extract the predictions into a sorted array
def process_number(sorted_prediction, top_city, game_round):
    global sorted_action_numbers

    sorted_action_numbers = sorted_prediction

    # Start recursive action search
    return choose(sorted_action_numbers[0], top_city, game_round)


def choose(action, city, game_round):
    global sorted_action_numbers

    points = game_round.points
    global_events = game_round.events
    cities = game_round.cities
    rounds = 1

    if action == 'applyHygienicMeasures':
        # Action: Apply hygienic measures

        if city.hygiene == '++' or city.hygiene == '++':
            # Pass if hygine is good
            pass
        else:
            # Preparing action
            action = ApplyHygienicMesaures(city)

            if action.getPoints() < points:
                # Return the action if enough points available
                return action
            else:
                # Saving the points if not enough available
                return EndRound()

    elif action == 'callElections':
        # Action: Call elections

        if city.government == '++' or city.government == '++':
            # Pass if govenment is good
            pass
        else:
            # Preparing action
            action = CallElections(city)

            if action.getPoints() < points:
                # Return the action if enough points available
                return action
            else:
                # Saving the points if not enough available
                return EndRound()

    elif action == 'closeAirport':
        # Action: Close Airport

        if any(isinstance(x, AirportClosed) for x in city.events):
            # Pass if airport already closed
            pass
        else:
            # Calculating maximal amount of rounds
            rounds = CloseAirport.calculateRounds(points)

            if rounds < 2:
                return EndRound()
            else:
                # Preparing action
                action = CloseAirport(city, rounds)

                if action.getPoints() < points:
                    # Return the action if enough points available
                    return action
                else:
                    # Saving the points if not enough available
                    return EndRound()

    elif action == 'closeConnection':
        # Action: Close Airport Connection

        if any(isinstance(x, AirportClosed) for x in city.events):
            # Pass if airport is already closed
            pass
        else:
            # If connections are available
            if len(city.connections) != 0:

                already_closed = []
                possible_cities = []

                # Find already closed connections
                for x in city.events:
                    if isinstance(x, ConnectionClosed):
                        already_closed.append(x.city)

                # Find possible connections
                for y in city.connections:
                    if y not in already_closed:
                        for z in cities:
                            if z.name == y:
                                possible_cities.append(z)

                try:
                    # Choose connection with bad score
                    connection = sorted(possible_cities, key=lambda a: a.score,
                                        reverse=True).pop(1)
                except IndexError:
                    # If no connection is suitable choose another action
                    index = numpy.argwhere(sorted_action_numbers == action)
                    sorted_action_numbers = numpy.delete(sorted_action_numbers, index)
                    action = sorted_action_numbers[0]
                    return choose(action, city, game_round)

                # Calculating maximal amount of rounds
                rounds = CloseConnection.calculateRounds(points)

                # Preparing action
                action = CloseConnection(city, connection.name, rounds)

                if action.getPoints() < points:
                    # Return the action if enough points available
                    return action
                else:
                    # Saving the points if not enough available
                    return EndRound()

    elif action == 'medication':
        # Action: Develop/Deploy Medication

        outbreaks = []

        for x in city.events:
            if isinstance(x, Outbreak):
                outbreaks.append(x)

        sorted_outbreaks = sorted(outbreaks, key=lambda x: x.prevalence,
                                  reverse=True)

        for x in sorted_outbreaks:

            if x.prevalence < 0.2:
                x_already_in_development = False

                for y in global_events:
                    if isinstance(y, VaccineAvailable):
                        if x.pathogen.name == y.pathogen.name:
                            action = DeployVaccine(city, y.pathogen)
                            if action.getPoints() < points:
                                return action
                            else:
                                return EndRound()

                    elif isinstance(y,
                                    VaccineInDevelopment):
                        if x.pathogen.name == y.pathogen.name:
                            x_already_in_development = True
                            break

                if not x_already_in_development:
                    action = DevelopVaccine(x.pathogen)
                    if action.getPoints() < points:
                        return action
                    else:
                        return EndRound()

            else:
                x_already_in_development = False

                for y in global_events:
                    if isinstance(y,
                                  MedicationAvailable):
                        if x.pathogen.name == y.pathogen.name:
                            action = DeployMedication(city, y.pathogen)
                            if action.getPoints() < points:
                                return action
                            else:
                                return EndRound()

                    elif isinstance(y,
                                    MedicationInDevelopment):
                        if x.pathogen.name == y.pathogen.name:
                            x_already_in_development = True
                            break

                if not x_already_in_development:
                    action = DevelopMedication(x.pathogen)
                    if action.getPoints() < points:
                        return action
                    else:
                        return EndRound()

    elif action == 'vaccine':
        # Action: Develop/Deploy Vaccine

        outbreaks = []

        for x in city.events:
            if isinstance(x, Outbreak):
                outbreaks.append(x)

        sorted_outbreaks = sorted(outbreaks, key=lambda x: x.prevalence,
                                  reverse=True)

        for x in sorted_outbreaks:

            if x.prevalence > 0.8:
                x_already_in_development = False

                for y in global_events:
                    if isinstance(y,
                                  MedicationAvailable):
                        if x.pathogen.name == y.pathogen.name:
                            action = DeployMedication(city, y.pathogen)
                            if action.getPoints() < points:
                                return action
                            else:
                                return EndRound()

                    elif isinstance(y,
                                    MedicationInDevelopment):
                        if x.pathogen.name == y.pathogen.name:
                            x_already_in_development = True
                            break

                if not x_already_in_development:
                    action = DevelopMedication(x.pathogen)
                    if action.getPoints() < points:
                        return action
                    else:
                        return EndRound()

            else:

                x_already_in_development = False

                for y in global_events:
                    if isinstance(y, VaccineAvailable):
                        if x.pathogen.name == y.pathogen.name:
                            action = DeployVaccine(city, y.pathogen)
                            if action.getPoints() < points:
                                return action
                            else:
                                return EndRound()

                    elif isinstance(y,
                                    VaccineInDevelopment):
                        if x.pathogen.name == y.pathogen.name:
                            x_already_in_development = True
                            break

                if not x_already_in_development:
                    action = DevelopVaccine(x.pathogen)
                    if action.getPoints() < points:
                        return action
                    else:
                        return EndRound()

    elif action == 'exertInfluence':

        if city.economy == '++' or city.economy == '++':
            pass
        else:
            action = ExertInfluence(city)
            if action.getPoints() < points:
                return action
            else:
                # print('Not enough points')
                return EndRound()

    elif action == 'launchCampaign':

        if city.awareness == '++' or city.awareness == '+':
            pass
        else:
            action = LaunchCampaign(city)
            if action.getPoints() < points:
                return action
            else:
                # print('Not enough points')
                return EndRound()

    elif action == 'putUnderQuarantine':

        if any(isinstance(x, Quarantine) for x in city.events):
            pass

        else:
            rounds = PutUnderQuarantine.calculateRounds(points)
            if rounds < 2:
                return EndRound()
            else:
                action = PutUnderQuarantine(city, rounds)
                if action.getPoints() < points:
                    return action
                else:
                    # print('Not enough points')
                    return EndRound()

    # Removing the current best action if the chosen action was not possible
    index = numpy.argwhere(sorted_action_numbers == action)
    sorted_action_numbers = numpy.delete(sorted_action_numbers, index)

    try:
        # Pick the next best action
        action = sorted_action_numbers[0]
        # Restart the method with this action
        return choose(action, city, game_round)
    except IndexError:
        # If no action was suitable
        return EndRound()
    except RecursionError:
        # If no action was suitable
        return EndRound()
