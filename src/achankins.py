from src.strategies import Strategy
from src.piece import Piece
from src.compare_all_moves_strategy import CompareAllMoves

import src.weight
import src.hash

class player1_achankins(CompareAllMoves):

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
                       float(weight_list[8]) * (board_stats['num_locations_with_two_pieces'] / 7.0)

        return board_value