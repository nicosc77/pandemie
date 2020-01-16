from model.events import Outbreak, BioTerrorrism, AntiVaccinationism, \
    LargeScalePanic, Quarantine, EconomicCrisis, \
    ConnectionClosed, \
    AirportClosed, Uprising, CampaignLaunched, MedicationDeployed, \
    MedicationInDevelopment, MedicationAvailable, \
    HygienicMeasuresApplied, VaccineInDevelopment, VaccineAvailable, \
    VaccineDeployed, ElectionsCalled, \
    InfluenceExcerted, PathogenEncountered


def process_event(data):
    # Global events
    if data['type'] == 'pathogenEncountered':
        return PathogenEncountered(data)

    elif data['type'] == 'economicCrisis':
        return EconomicCrisis(data)

    # Local events
    elif data['type'] == 'largeScalePanic':
        return LargeScalePanic(data)

    elif data['type'] == 'outbreak':
        return Outbreak(data)

    elif data['type'] == 'antiVaccinationism':
        return AntiVaccinationism(data)

    elif data['type'] == 'bioTerrorism':
        return BioTerrorrism(data)

    elif data['type'] == 'airportClosed':
        return AirportClosed(data)

    elif data['type'] == 'medicationInDevelopment':
        return MedicationInDevelopment(data)

    elif data['type'] == 'vaccineInDevelopment':
        return VaccineInDevelopment(data)

    elif data['type'] == 'vaccineAvailable':
        return VaccineAvailable(data)

    elif data['type'] == 'medicationAvailable':
        return MedicationAvailable(data)

    elif data['type'] == 'medicationDeployed':
        return MedicationDeployed(data)

    elif data['type'] == 'vaccineDeployed':
        return VaccineDeployed(data)

    elif data['type'] == 'connectionClosed':
        return ConnectionClosed(data)

    elif data['type'] == 'quarantine':
        return Quarantine(data)

    elif data['type'] == 'uprising':
        return Uprising(data)

    elif data['type'] == 'hygienicMeasuresApplied':
        return HygienicMeasuresApplied(data)

    elif data['type'] == 'influenceExerted':
        return InfluenceExcerted(data)

    elif data['type'] == 'campaignLaunched':
        return CampaignLaunched(data)

    elif data['type'] == 'electionsCalled':
        return ElectionsCalled(data)

    else:
        raise Exception('Unknown Event: ' + data['type'] + ', ' + str(data))
