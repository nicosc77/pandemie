import os

import numpy as np
from keras.layers import Dense, Dropout
from keras.models import Sequential
from keras.models import model_from_json

import app
from model.actions import EndRound
from processors import actionrandomizer, actionparser, cityprocessor

previous_city = {}
training_data = []
action = {}
previous_round = 1
trained_model = {}
model_loaded = False


# Collecting training data
def collect(game_round):
    global previous_city
    global action
    global previous_round

    # Checking if this is a new round and ending the round if not
    if game_round.round > previous_round:
        app.log.info('New round detected')
        previous_round = game_round.round

        # Checking if a action was actively applied to a city in the last round
        if previous_city:
            app.log.info(
                'Data of last round available, checking if positive effect')
            current_score = next((city for city in game_round.cities if
                                  city.name == previous_city.name),
                                 None).score
            # TODO: Find the magic number
            # print(previous_city.score - current_score)
            if current_score + 0.4 < previous_city.score:
                effect = previous_city.score - current_score
                if not isinstance(action, EndRound):
                    app.log.info('Action ' + str(
                        action.getMessage()) + ' had positive effect (' + str(
                        effect) + '), adding to training data')
                    training_data.append(
                        [cityprocessor.process_city(previous_city),
                         action.getLabel()])
                else:
                    app.log.info('Action was EndRound, not adding data')
            else:
                app.log.info(
                    'Action had no postive effect, not adding data')

        else:
            app.log.info('No valid action data of last round available')

        app.log.info('Randomizing next action')
        top_city = sorted(game_round.cities, key=lambda city: city.score,
                          reverse=True).pop(1)
        previous_city = top_city
        action = actionrandomizer.next_action(top_city, game_round.points,
                                              game_round.events,
                                              game_round.cities)
        app.log.info('Action is: ' + str(action.getMessage()))
        return action

    elif game_round.round == 1:
        previous_round = game_round.round
        app.log.info('First round detected, passing')
        return EndRound()

    elif game_round.round == previous_round:
        previous_round = game_round.round
        app.log.info(
            'Same round detected, ending round to complete collection of data')
        return EndRound()

    elif game_round.round < previous_round:
        # The game_round doesnt match to the current game
        # (Either this is a new game or the current game was aborted)
        app.log.info('Detected new game, resetting')
        previous_city = {}
        action = {}
        previous_round = 1
        return EndRound()


def play(game_round):
    global trained_model
    global action

    app.log.info('Picking top city')
    top_city = sorted(game_round.cities, key=lambda city: city.score,
                      reverse=True).pop(1)

    app.log.info('Processing city')
    observation = cityprocessor.process_city(top_city)

    app.log.info('Predicting action')
    result = \
        trained_model.predict(observation.reshape(-1, len(observation)))[
            0]

    app.log.info('Processing results from prediction')
    action = actionparser.process_number(result, top_city,
                                         game_round.events,
                                         game_round.points,
                                         game_round.round,
                                         game_round.cities)
    app.log.info('Action is: ' + str(action.getMessage()))

    return action


def build_model(input_size, output_size):
    app.log.info('Building model')

    model = Sequential()
    model.add(Dense(128, input_dim=input_size, activation='relu'))
    model.add(Dropout(0.3))
    model.add(Dense(64, activation='relu'))
    model.add(Dropout(0.3))
    model.add(Dense(output_size, activation='softmax'))
    model.compile(optimizer='adam', loss='categorical_crossentropy',
                  metrics=['accuracy'])
    return model


def train_model(epochs):
    global training_data
    global trained_model
    global model_loaded

    app.log.info('Training model')
    x = np.array([i[0] for i in training_data]).reshape(-1, len(
        training_data[0][0]))
    y = np.array([i[1] for i in training_data]).reshape(-1, len(
        training_data[0][1]))

    model = build_model(input_size=len(x[0]), output_size=len(y[0]))

    model.summary()

    model.fit(x, y, batch_size=6000, verbose=1, validation_split=0.25,
              shuffle=True, epochs=epochs)

    trained_model = model
    model_loaded = True
    return model


def save_model():
    global trained_model

    # serialize model to JSON
    model_json = trained_model.to_json()
    path = os.path.dirname(os.path.abspath(__file__)) + '/models/'
    with open(path + "model.json", "w") as json_file:
        json_file.write(model_json)

    # serialize weights to HDF5
    trained_model.save_weights(path + "model.h5")

    app.log.info("Saved model to disk")


def load_model():
    global trained_model
    global model_loaded

    if not model_loaded:

        try:
            # load json and create model
            path = os.path.dirname(os.path.abspath(__file__)) + '/models/'
            json_file = open(path + 'model.json', 'r')
            loaded_model_json = json_file.read()
            json_file.close()
            trained_model = model_from_json(loaded_model_json)

            # load weights into new model
            trained_model.load_weights(path + "model.h5")

            app.log.info('Loaded model from disk')
            model_loaded = True
            return True

        except FileNotFoundError:
            app.log.info('Cannot load model')
            return False

    else:
        app.log.info('Model already loaded')
        return True
