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

        board_value =  1.00 * board_stats['sum_distances']                      + \
                       0.00 * board_stats['number_of_singles']                  + \
                       0.00 * board_stats['number_occupied_spaces']             + \
                       0.00 * board_stats['opponents_taken_pieces']             + \
                       0.00 * board_stats['sum_distances_to_endzone']           + \
                       0.00 * board_stats['sum_single_distance_away_from_home'] + \
                       0.00 * board_stats['pieces_on_board']                    + \
                       0.00 * board_stats['sum_distances_opponent']
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