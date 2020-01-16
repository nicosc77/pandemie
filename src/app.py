import logging
import os
import platform
import subprocess

from flask import Flask, request

from model.gameround import GameRound
from net import net
from processors.scoring import score

app = Flask(__name__)

# Default configurations
port = 5000
log = logging.getLogger('werkzeug')


# Developer Endpoint for testing th net
@app.route('/dev/test', methods=['POST'])
def testNet():
    if app.debug:
        if request.method == 'POST':
            log.info('Receiving request to perform model testing')

            # Very ugly workaround because keras in this version
            # is messing up with tensorflow when multithreading is enabled
            import keras.backend.tensorflow_backend as tb
            # noinspection PyProtectedMember
            tb._SYMBOLIC_SCOPE.value = True

            # Loading trained model if available
            net.load_model()

            # Testing
            count = request.args.get('count', default=1, type=int)
            log.info('Testing with ' + str(count) + ' rounds...')

            if platform.system() == 'Darwin':
                path = os.path.dirname(
                    os.path.abspath(__file__)) + '/bin/ic20_darwin'
            elif platform.system() == 'Linux':
                path = os.path.dirname(
                    os.path.abspath(__file__)) + '/bin/ic20_linux'
            else:
                path = os.path.dirname(
                    os.path.abspath(__file__)) + '/bin/ic20_windows'

            results = []
            for i in range(count):
                process = subprocess.run([path, '-u',
                                          'http://localhost:' + str(
                                              port) + '/dev/api/test', '-t',
                                          '0'],
                                         encoding='utf-8',
                                         stdout=subprocess.PIPE)
                if 'win' in str(process.stdout):
                    results.append('win')
                    log.info('Performed test with outcome: Win')
                elif 'loss' in str(process.stdout):
                    results.append('loss')
                    log.info('Performed test with outcome: Loss')
            wins = results.count("win")
            losses = results.count("loss")
            log.info('Completed test with following results: ' + str(
                wins / len(results) * 100) + '% win, ' + str(
                losses / len(results) * 100) + '% loss ')
            return 'Ok'
    else:
        return 'This endpoint is only available in development mode'


# Developer Endpoint for training the model
@app.route('/dev/train', methods=['POST'])
def trainNet():
    if app.debug:
        if request.method == 'POST':
            log.info('Receiving request to perform model training')

            # Very ugly workaround because keras in this version
            # is messing up with tensorflow when multithreading is enabled
            import keras.backend.tensorflow_backend as tb
            # noinspection PyProtectedMember
            tb._SYMBOLIC_SCOPE.value = True

            # Collecting
            count = request.args.get('count', default=1, type=int)
            log.info('Collecting data with ' + str(count) + ' rounds...')

            for i in range(count):
                log.info(str(i) + ' of ' + str(count) + ' games played')
                if platform.system() == 'Darwin':
                    path = os.path.dirname(
                        os.path.abspath(__file__)) + '/bin/ic20_darwin'
                elif platform.system() == 'Linux':
                    path = os.path.dirname(
                        os.path.abspath(__file__)) + '/bin/ic20_linux'
                else:
                    path = os.path.dirname(
                        os.path.abspath(__file__)) + '/bin/ic20_windows'
                subprocess.run([path, '-u', 'http://localhost:' + str(
                    port) + '/dev/api/collect', '-t', '0'],
                               stdout=subprocess.DEVNULL)
            log.info('Collecting complete')

            # Training
            epochs = request.args.get('epochs', default=100, type=int)
            log.info('Starting training with ' + str(epochs) + ' epochs...')
            net.train_model(epochs)
            log.info('Training complete')

            # Saving the trained model and resetting Loading indicator
            net.save_model()

            return 'Ok'
    else:
        return 'This endpoint is only available in development mode'


# Endpoint for collecting training data with random game actions
@app.route('/dev/api/collect', methods=['POST'])
def collectModel():
    if app.debug:
        if request.method == 'POST':
            # Parsing Data
            log.info('Parsing the json data')
            game_round = GameRound(request.json)
            log.info('Receiving request to collect round ' + str(
                game_round.round) + ' of a game')

            # Calculating scores
            log.info('Calculating scores for the gameround')
            game_round = score(game_round)

            # Collect training data
            action = net.collect(game_round)
            # Returning the action
            return action.getMessage()
    else:
        return 'This endpoint is only available in development mode'


# Endpoint for testing the model
@app.route('/dev/api/test', methods=['POST'])
def testModel():
    if app.debug:
        if request.method == 'POST':
            # Very ugly workaround because keras in this version
            # is messing up with tensorflow when multithreading is enabled
            import keras.backend.tensorflow_backend as tb
            # noinspection PyProtectedMember
            tb._SYMBOLIC_SCOPE.value = True

            # Parsing Data
            log.info('Parsing the json data')
            game_round = GameRound(request.json)
            log.info('Receiving request to collect round ' + str(
                game_round.round) + ' of a game')

            # Load model if not alredy loaded
            net.load_model()

            # Calculating scores
            log.info('Calculating scores for the gameround')
            game_round = score(game_round)

            # Compute the action
            action = net.play(game_round)

            # Returning the action
            return action.getMessage()
    else:
        return 'This endpoint is only available in development mode'


# Main endpoint for production
@app.route('/', methods=['POST', 'GET'])
def main():

    # Very ugly workaround because keras in this version
    # is messing up with tensorflow when multithreading is enabled
    import keras.backend.tensorflow_backend as tb
    # noinspection PyProtectedMember
    tb._SYMBOLIC_SCOPE.value = True

    if request.method == 'POST':
        # Load model if not alredy loaded
        net.load_model()

        # Parsing Data & Calculating scores
        game_round = score(GameRound(request.json))

        # Compute the action
        action = net.play(game_round)
        # Returning the action
        return action.getMessage()

    elif request.method == 'GET':
        # Load model if not alredy loaded
        if net.load_model():
            net.trained_model.summary()
            return 'Services running, model loaded'
        else:
            return 'Services running, no model present'


if __name__ == '__main__':
    debug_env = False
    try:
        if os.environ['DEBUG'] == 'True':
            debug_env = True
            log.setLevel(logging.INFO)
        else:
            debug_env = False
            log.setLevel(logging.ERROR)
    except KeyError:
        pass

    app.run(debug=debug_env, port=5000)
