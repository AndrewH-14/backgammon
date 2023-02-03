from src.strategies import Strategy
from src.piece import Piece
from src.compare_all_moves_strategy import CompareAllMoves

import src.weight

# Default features to be used in the weighting function

# 'number_occupied_spaces': number_occupied_spaces,
# The number of spaces that your pieces are currently occupying with more than one piece

# 'opponents_taken_pieces': opponents_taken_pieces,
# The number of opponent's pieces we currently have taken

# 'sum_distances': sum_distances,
# The sum of your pieces distances to the very end of the board

# 'sum_distances_opponent': sum_distances_opponent,
# The sum of the opponents pieces distances to the very end of the board

# 'number_of_singles': number_of_singles,
# The amount of spaces we occupy with only one piece on them

# 'sum_single_distance_away_from_home': sum_single_distance_away_from_home,
# The sum of your single pieces distance to the very end of the board

# 'pieces_on_board': pieces_on_board,
# The number of pieces that you currently have on the board.

# 'sum_distances_to_endzone': sum_distances_to_endzone,
# The sum of your pieces distances to the start of the endzone

class player1_achankins(CompareAllMoves):

    # Function that will evaluate the board
    def evaluate_board(self, myboard, colour):
        board_stats = self.assess_board(colour, myboard)

        # Attempt to normalize the features between a value of 0...1 and weight them
        board_value =  0.75 * (board_stats['sum_distances'] / 163.0)                      + \
                      -0.75 * (board_stats['number_of_singles'] / 7.0)                    + \
                      -0.75 * (board_stats['number_occupied_spaces'] / 7.0)               + \
                      -0.25 * (board_stats['opponents_taken_pieces'] / 1.0)               + \
                       0.9  * (board_stats['sum_distances_to_endzone'] / 75.0)            + \
                       0.9  * (board_stats['sum_single_distance_away_from_home'] / 100.0) + \
                       1.0  * (board_stats['pieces_on_board'] / 15.0)                     + \
                      -1.0  * (board_stats['sum_distances_opponent'] / 163.0)
        return board_value

class player2_achankins(CompareAllMoves):

    # Default features plus the new novel feature to be created

    def evaluate_board(self, myboard, colour):
        board_stats = self.assess_board(colour, myboard)

        weight_list = src.weight.weight

        # Attempt to normalize the features between a value of 0...1 and weight them
        board_value =  float(weight_list[0]) * (board_stats['sum_distances'] / 163.0)                      + \
                       float(weight_list[1]) * (board_stats['number_of_singles'] / 7.0)                    + \
                       float(weight_list[2]) * (board_stats['number_occupied_spaces'] / 7.0)               + \
                       float(weight_list[3]) * (board_stats['opponents_taken_pieces'] / 1.0)               + \
                       float(weight_list[4])  * (board_stats['sum_distances_to_endzone'] / 75.0)            + \
                       float(weight_list[5])  * (board_stats['sum_single_distance_away_from_home'] / 100.0) + \
                       float(weight_list[6])  * (board_stats['pieces_on_board'] / 15.0)                     + \
                       float(weight_list[7])  * (board_stats['sum_distances_opponent'] / 163.0)             + \
                       float(weight_list[8]) * (board_stats['num_pieces_in_best_locations'] / 15.0)
        return board_value