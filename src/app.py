import logging

from flask import Flask, request

from model.gameround import GameRound
from processors.scoring import score
from solver.collector import Collector
from solver.solver import Solver

app = Flask(__name__)

# Default configurations
port = 5000
log = logging.getLogger('werkzeug')
collector = Collector()
solver = Solver()


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
    global solver
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
    debug_env = True
    log.setLevel(logging.INFO)
    app.run(debug=debug_env, host="0.0.0.0", port=5000)
