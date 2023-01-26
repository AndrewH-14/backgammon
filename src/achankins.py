from src.strategies import Strategy
from src.piece import Piece
from src.compare_all_moves_strategy import CompareAllMoves

class player1_achankins(CompareAllMoves):

    # Default features to be used in the weighting function
    # 'number_occupied_spaces': number_occupied_spaces,
    # 'opponents_taken_pieces': opponents_taken_pieces,
    # 'sum_distances': sum_distances,
    # 'sum_distances_opponent': sum_distances_opponent,
    # 'number_of_singles': number_of_singles,
    # 'sum_single_distance_away_from_home': sum_single_distance_away_from_home,
    # 'pieces_on_board': pieces_on_board,
    # 'sum_distances_to_endzone': sum_distances_to_endzone,

    # Function that will evaluate the board
    def evaluate_board(self, myboard, colour):
        board_stats = self.assess_board(colour, myboard)

        weight_file = open("weights.txt", "r")
        string_weights = weight_file.read()
        weight_list = string_weights.split(",")
        weight_file.close()

        board_value = float(weight_list[0]) * board_stats['sum_distances']                      + \
                      float(weight_list[1]) * board_stats['number_of_singles']                  + \
                      float(weight_list[2]) * board_stats['number_occupied_spaces']             + \
                      float(weight_list[3]) * board_stats['opponents_taken_pieces']             + \
                      float(weight_list[4]) * board_stats['sum_distances_to_endzone']           + \
                      float(weight_list[5]) * board_stats['sum_single_distance_away_from_home'] + \
                      float(weight_list[6]) * board_stats['pieces_on_board']                    + \
                      float(weight_list[7]) * board_stats['sum_distances_opponent']
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

        board_value = board_stats['sum_distances'] + 2 * board_stats['number_of_singles'] - \
                      board_stats['number_occupied_spaces'] - board_stats['opponents_taken_pieces']
        # board_value = board_stats[NOVEL_FEATURE] * 2 + board_stats['sum_distances'] + 2 * board_stats['number_of_singles'] - \
        #               board_stats['number_occupied_spaces'] - board_stats['opponents_taken_pieces']
        return board_value