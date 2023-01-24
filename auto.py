from random import randint
import sys
from src.colour import Colour
from src.game import Game
from src.strategy_factory import StrategyFactory
from src.strategies import HumanStrategy

if __name__ == '__main__':

    #strategy_index1 = int(input('Pick strategy 1:\n'))
    chosen_strategy1 = StrategyFactory.create_by_name(sys.argv[1])

    #strategy_index2 = int(input('Pick strategy 2:\n'))
    chosen_strategy2 = StrategyFactory.create_by_name(sys.argv[2])

    game = Game(
        white_strategy=chosen_strategy1,
        black_strategy=chosen_strategy2,
        first_player=Colour(randint(0, 1))
    )

    #print("White Strategy: " + sys.argv[1])
    #print("Black Strategy: " + sys.argv[2])

    if (len(sys.argv) > 3 and sys.argv[3].lower() == 'true'):
        # print("verbose=true")
        game.run_game(verbose=True)
    else:
        # print("verbose=false")
        game.run_game(verbose=False)
    print("%s won!" % game.who_won())
    # game.board.print_board()
