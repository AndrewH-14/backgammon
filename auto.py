from random import randint
import sys
from src.colour import Colour
from src.game import Game
from src.strategy_factory import StrategyFactory
from src.strategies import HumanStrategy

import src.weight

import os
import threading
import sys

# Get the program ID, start idx, and end idx
prog_id   = sys.argv[1]
start_idx = int(sys.argv[2])
end_idx   = int(sys.argv[3])

# Read in the potential weight combinations to be tested
weight_combination_file = open("combinations.txt", "r")
weight_combination_string = weight_combination_file.read()
weight_combination_list = weight_combination_string.split("\n")
weight_combination_list_len = len(weight_combination_list)

# Create the thread class and give it a start and end index for the combination file.
class thread():
    start_idx = 0
    end_idx = 0
    num_games = 0
    def __init__(self, thread_name, thread_ID, start_idx, end_idx, num_games):
        # threading.Thread.__init__(self)
        self.thread_name = thread_name
        self.thread_ID = thread_ID
        self.start_idx = start_idx
        self.end_idx = end_idx
        self.num_games = num_games

    def run(self):
        # Print off the
        # Store the results file name
        final_file_name = self.thread_name + "-results-" + prog_id + ".txt"
        final_file = open(final_file_name, "w")
        final_file.close()
        # Iterate through the lines that this thread is responsible for
        for idx in range(self.start_idx, self.end_idx + 1):
            # Win count variables
            white_win_count = 0
            win_percentage  = 0.0
            # Run the desired number of games and check the win percentage
            for game_idx in range(0, self.num_games):
                # Initialize the game object
                game = Game(
                    white_strategy=StrategyFactory.create_by_name("player1_achankins"),
                    black_strategy=StrategyFactory.create_by_name("CompareAllMovesWeightingDistance"),
                    first_player=Colour(randint(0, 1))
                )

                # If the win percentage is less than 10 percent halfway through
                # the weight test, move on to the next weight
                if game_idx == (self.num_games // 2):
                    if win_percentage < 0.10:
                        break

                # If the win percentage is less than 15 through 3/4 through the
                # weight test, move on to the next weight
                if game_idx == ((self.num_games * 3) // 4):
                    if win_percentage < 0.10:
                        break

                # Remove the brackets from the line
                line = weight_combination_list[idx].replace("[", "")
                line = line.replace("]", "")
                line = line.replace(" ", "")
                src.weight.init(line)

                # Run the backgammon game and output results to the output file
                game.run_game(verbose=False)
                if "white" == game.who_won():
                    white_win_count += 1
                    win_percentage = white_win_count / game_idx

            # If the current weight has a win percentage over 50 record it
            if (win_percentage > 0.0):
                final_file_name = self.thread_name + "-results-" + prog_id + ".txt"
                final_file = open(final_file_name, "a")
                final_file.write(line + "\n" + str(win_percentage) + "\n")
                final_file.close()

if __name__ == '__main__':

    # Initialize the thread and start it
    thread1 = thread("thread1", 1, start_idx, end_idx, 50)
    thread1.run()