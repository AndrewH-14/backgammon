import queue
import threading

from flask import Flask, request
from flask_cors import CORS, cross_origin
from src.colour import Colour
from src.compare_all_moves_strategy import CompareAllMovesSimple
from src.game import Game
from random import randint
from src.strategies import Strategy

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

moves_to_make = queue.Queue()
move_results = queue.Queue()
current_board = []
current_move = []


def game_thread():
    class ApiStrategy(Strategy):
        def move(self, board, colour, dice_roll, make_move):
            current_move.insert(0, dice_roll)
            while len(dice_roll) > 0:
                try:
                    move = moves_to_make.get()
                    make_move(move['location'], move['die_roll'])
                    dice_roll.remove(move['die_roll'])
                    move_results.put("done")
                except:
                    move_results.put("fail")

    game = Game(
        white_strategy=ApiStrategy(),
        black_strategy=CompareAllMovesSimple(),
        first_player=Colour(randint(0, 1))
    )
    current_board.append(game.board)
    game.run_game()


threading.Thread(target=game_thread).start()


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/start-game')
@cross_origin()
def start_game():
    return {'board': current_board[0].to_json(),
            'dice_roll': current_move[0]}


@app.route('/move-piece')
@cross_origin()
def move_piece():
    location = request.args.get('location', default=1, type=int)
    die_roll = request.args.get('die-roll', default=1, type=int)
    moves_to_make.put({
        'location': location,
        'die_roll': die_roll
    })
    move_results.get()
    return current_board[0].to_json()
