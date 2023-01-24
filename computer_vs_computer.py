from random import randint

from src.colour import Colour
from src.game import Game
from src.strategy_factory import StrategyFactory
from src.strategies import HumanStrategy

if __name__ == '__main__':

    print("Available Strategies:")
    strategies = [x for x in StrategyFactory.get_all() if x.__name__ != HumanStrategy.__name__]
    for i, strategy in enumerate(strategies):
        print("[%d] %s (%s)" % (i, strategy.__name__, strategy.get_difficulty()))

    strategy_index1 = int(input('Pick strategy 1:\n'))
    chosen_strategy1 = StrategyFactory.create_by_name(strategies[strategy_index1].__name__)

    strategy_index2 = int(input('Pick strategy 2:\n'))
    chosen_strategy2 = StrategyFactory.create_by_name(strategies[strategy_index2].__name__)

    game = Game(
        white_strategy=chosen_strategy1,
        black_strategy=chosen_strategy2,
        first_player=Colour(randint(0, 1))
    )

    game.run_game(verbose=True)

    print("White Strategy: "+strategies[strategy_index1].__name__);
    print("Black Strategy: "+strategies[strategy_index2].__name__);

    print("%s won!" % game.who_won())
    game.board.print_board()
