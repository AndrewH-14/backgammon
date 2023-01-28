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
# python3 auto.py <prog_id> <num_prog>
prog_id_int = int(sys.argv[1])
prog_id_str = sys.argv[1]
num_prog    = int(sys.argv[2])

# Generate weigths and store them in a list
"""
res = [[a, b, c, d, e, f, g, h] for a in [-1, 0, 1]
                                for b in [-1, 0, 1]
                                for c in [-1, 0, 1]
                                for d in [-1, 0, 1]
                                for e in [-1, 0, 1]
                                for f in [-1, 0, 1]
                                for g in [-1, 0, 1]
                                for h in [-1, 0, 1]]
"""

# Get the weights from a file
res = []
combination_file = open("final_results.txt", "r")
while True:
    weight = combination_file.readline()
    if weight == "":
        break
    weight = weight.replace("[", "")
    weight = weight.replace("]", "")
    weight_list = weight.split(",")
    res.append([float(weight_list[0]), float(weight_list[1]), float(weight_list[2]), float(weight_list[3]),
                float(weight_list[4]), float(weight_list[5]), float(weight_list[6]), float(weight_list[7])])
combination_file.close()

# Compute the start and end index
num_weights = len(res)
print(num_weights)
section_len = num_weights // num_prog
start_idx   = (section_len * prog_id_int)
end_idx = 0
if num_prog == (prog_id_int + 1):
    end_idx = num_weights - 1
else:
    end_idx = (section_len * prog_id_int) + section_len - 1

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
        final_file_name = self.thread_name + "-results-" + prog_id_str + ".txt"
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
                    black_strategy=StrategyFactory.create_by_name("MoveFurthestBackStrategy"),
                    first_player=Colour(randint(0, 1))
                )

                # If the win percentage is less than 10 percent halfway through
                # the weight test, move on to the next weight
                # if game_idx == (self.num_games // 2):
                #     if win_percentage < 0.10:
                #         break

                # If the win percentage is less than 15 through 3/4 through the
                # weight test, move on to the next weight
                # if game_idx == ((self.num_games * 3) // 4):
                #     if win_percentage < 0.10:
                #         break

                # Remove the brackets from the line
                src.weight.init(res[idx])
                # Run the backgammon game and output results to the output file
                game.run_game(verbose=False)
                if "white" == str(game.who_won()):
                    print("white won " + str(idx))
                    white_win_count += 1
                    # win_percentage = white_win_count / (game_idx + 1)
                else:
                    print("black won " + str(idx))

            print("###########################################################")
            # If the current weight has a win percentage over 50 record it
            win_percentage = white_win_count / self.num_games
            if (win_percentage > 0.50):
                final_file_name = self.thread_name + "-results-" + prog_id_str + ".txt"
                final_file = open(final_file_name, "a")
                final_file.write(str(res[idx]) + "\n" + str(win_percentage) + "\n")
                final_file.close()

if __name__ == '__main__':

    # Initialize the thread and start it
    thread1 = thread("thread1", 1, start_idx, end_idx, 600)
    thread1.run()
