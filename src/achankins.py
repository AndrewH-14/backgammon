from src.strategies import Strategy
from src.piece import Piece
from src.compare_all_moves_strategy import CompareAllMoves

import src.weight

class player1_achankins(CompareAllMoves):

    # Default features to be used in the weighting function

    # 'number_occupied_spaces': number_occupied_spaces,
    # The number of spaces that your pieces are currently occupying
    # NOTE: This does not include spaces with only a single piece on them

    # 'opponents_taken_pieces': opponents_taken_pieces,
    # The number of opponent's pieces we currently have taken
    # NOTE: We would prefer to take as many pieces as possible.
    # NOTE: Due to this, we want this parameter to strongly count towards the value

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
    # NOTE: We would prefer fewer pieces to be on the board because it means that
    #       some of the pieces have reached the very end.
    # NOTE: Due to this, we want this parameter to count against the value

    # 'sum_distances_to_endzone': sum_distances_to_endzone,
    # The sum of your pieces distances to the start of the endzone

    # Function that will evaluate the board
    def evaluate_board(self, myboard, colour):
        board_stats = self.assess_board(colour, myboard)

        # Create a list of weights from the passed in string
        # weight_list = src.weight.weight.split(",")
        weight_list = src.weight.weight
        # print("Weight used: " + str(weight_list))

        # Attempt to normalize the features between a value of 0...1 and weight them
        board_value = float(weight_list[0]) * (board_stats['sum_distances'] / 163.0)                      + \
                      float(weight_list[1]) * (board_stats['number_of_singles'] / 7.0)                    + \
                      float(weight_list[2]) * (board_stats['number_occupied_spaces'] / 7.0)               + \
                      float(weight_list[3]) * (board_stats['opponents_taken_pieces'] / 1.0)               + \
                      float(weight_list[4]) * (board_stats['sum_distances_to_endzone'] / 75.0)            + \
                      float(weight_list[5]) * (board_stats['sum_single_distance_away_from_home'] / 100.0) + \
                      float(weight_list[6]) * (board_stats['pieces_on_board'] / 15.0)                     + \
                      float(weight_list[7]) * (board_stats['sum_distances_opponent'] / 163.0)

        # board_value = float(weight_list[0]) * (board_stats['sum_distances'])                      + \
        #               float(weight_list[1]) * (board_stats['number_of_singles'])                  + \
        #               float(weight_list[2]) * (board_stats['number_occupied_spaces'])             + \
        #               float(weight_list[3]) * (board_stats['opponents_taken_pieces'])             + \
        #               float(weight_list[4]) * (board_stats['sum_distances_to_endzone'])           + \
        #               float(weight_list[5]) * (board_stats['sum_single_distance_away_from_home']) + \
        #               float(weight_list[6]) * (board_stats['pieces_on_board'])                    + \
        #               float(weight_list[7]) * (board_stats['sum_distances_opponent'])
        return board_value

class player2_achankins(CompareAllMoves):

    # Default features plus the new novel feature to be created
    # 'NOVEL_FEATURE': novel_feature_value,
    # 'number_occupied_spaces': number_occupied_spaces,
    # 'opponents_taken_pieces': opponents_taken_pieces,
    # 'sum_distances': sum_distances,
    # 'sum_distances_opponent': sum_distances_opponent,
    # 'number_of_singles': number_of_singles,
    # 'sum_single_distance_away_from_home': sum_single_distance_away_from_home,
    # 'pieces_on_board': pieces_on_board,
    # 'sum_distances_to_endzone': sum_distances_to_endzone,

    def evaluate_board(self, myboard, colour):
        board_stats = self.assess_board(colour, myboard)

        #board_value = board_stats['sum_distances'] + 2 * board_stats['number_of_singles'] - \
                      #board_stats['number_occupied_spaces'] - board_stats['opponents_taken_pieces']
        # board_value = board_stats[NOVEL_FEATURE] * 2 + board_stats['sum_distances'] + 2 * board_stats['number_of_singles'] - \
        #               board_stats['number_occupied_spaces'] - board_stats['opponents_taken_pieces']
        return 0