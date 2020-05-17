import logging
import platform
import subprocess
from pathlib import Path

from flask import Flask, request

from model.gameround import GameRound
from processors.scoring import score
from solver.collector import Collector
from solver.solver import Solver

app = Flask(__name__)

# Default configurations
port = 5000
log = logging.getLogger('werkzeug')
solver = Solver()
collector = Collector()


# Endpoint for collecting training data with random game actions
@app.route('/collect', methods=['POST'])
def collect_model():

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
            action = collector.collect(game_round)

            # Returning the action
            message = action.getMessage()
            log.info('Action is' + str(message))
            return message
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
        # Parsing Data & Calculating scores
        game_round = score(GameRound(request.json))
        log.info('Receiving request to play round ' + str(
            game_round.round) + ' of a game')

        # Compute the action
        action = solver.test(game_round)

        # Returning the action
        message = action.getMessage()
        log.info('Action is' + str(message))
        return message


if __name__ == '__main__':
    debug_env = False
    try:

        debug_env = True
        log.setLevel(logging.INFO)

    except KeyError:
        pass

    app.run(debug=debug_env, port=5000)
