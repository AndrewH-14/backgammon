from src.strategies import Strategy
from src.piece import Piece


class CompareAllMoves(Strategy):

    @staticmethod
    def get_difficulty():
        return "Hard"

    # Function that generates the features to be used when calculating the best
    # possible move.
    def assess_board(self, colour, myboard):
        # Get the current location of the pieces on the board
        pieces = myboard.get_pieces(colour)
        # Get the number of pieces on the board
        pieces_on_board = len(pieces)
        # Initialize the features that will be returned by the function
        sum_distances = 0
        number_of_singles = 0
        number_occupied_spaces = 0
        sum_single_distance_away_from_home = 0
        sum_distances_to_endzone = 0
        num_locations_with_two_or_three_pieces = 0
        # Calculate the sum of the pieces distance to home and the sum of the
        # pieces distance to the endzone (last section of board)
        for piece in pieces:
            sum_distances = sum_distances + piece.spaces_to_home()
            if piece.spaces_to_home() > 6:
                sum_distances_to_endzone += piece.spaces_to_home() - 6
        # Get the number of single pieces, the sum of the single pieces distance
        # to home, and the number of occupied spaces.
        for location in range(1, 25):
            pieces = myboard.pieces_at(location)
            if len(pieces) != 0 and pieces[0].colour == colour:
                if len(pieces) == 1:
                    number_of_singles = number_of_singles + 1
                    sum_single_distance_away_from_home += 25 - pieces[0].spaces_to_home()
                elif len(pieces) > 1: # Not counting single spaces
                    number_occupied_spaces = number_occupied_spaces + 1
                if len(pieces) > 1 and len(pieces) <= 3:
                    num_locations_with_two_or_three_pieces += 1
        # Get the number of piece's we have taken from the opponent
        opponents_taken_pieces = len(myboard.get_taken_pieces(colour.other()))
        # Get the number of opponent's pieces on the board
        opponent_pieces = myboard.get_pieces(colour.other())
        # Get the sum of the opponents pieces to their home
        sum_distances_opponent = 0
        for piece in opponent_pieces:
            sum_distances_opponent = sum_distances_opponent + piece.spaces_to_home()

        """
        # Calculate the probability that our single pieces can be taken
        probability_piece_can_be_taken = 0
        for location in range(1, 25):
            pieces1 = myboard.pieces_at(location)
            if len(pieces1) == 1 and pieces1[0].colour == colour:
                for idx in range (25, location, -1):
                    if pieces1[0] != colour:
                        # Calculate the opponent is from our location
                        distance_to_single_piece = idx - location
                        if distance_to_single_piece == 12: # (1/36 chance)
                            probability_piece_can_be_taken += 1/36
                        elif distance_to_single_piece == 11: # (2/36 chance)
                            probability_piece_can_be_taken += 2/36
                        elif distance_to_single_piece == 10: # (3/36 chance)
                            probability_piece_can_be_taken += 3/36
                        elif distance_to_single_piece == 9: # (4/36 chance)
                            probability_piece_can_be_taken += 4/36
                        elif distance_to_single_piece == 8: # (5/36 chance)
                            probability_piece_can_be_taken += 5/36
                        elif distance_to_single_piece == 7: # (6/36 chance)
                            probability_piece_can_be_taken += 6/36
                        elif distance_to_single_piece == 6: # (5/36 chance)
                            probability_piece_can_be_taken += 5/36
                        elif distance_to_single_piece == 5: # (4/36 chance)
                            probability_piece_can_be_taken += 4/36
                        elif distance_to_single_piece == 4: # (3/36 chance)
                            probability_piece_can_be_taken += 3/36
                        elif distance_to_single_piece == 3: # (2/36 chance)
                            probability_piece_can_be_taken += 2/36
                        elif distance_to_single_piece == 2: # (1/36 chance)
                            probability_piece_can_be_taken += 1/36
        """

        # New feature calculation (Pieces in best quadrant)
        """
        num_pieces_in_best_locations = 0
        for location in range(1, 25):
            pieces = myboard.pieces_at(location)
            if len(pieces) > 1 and len(pieces) <=3 and ((location == 5) or (location == 20)):
                num_pieces_in_best_locations += 1
        """

        return {
            'number_occupied_spaces': number_occupied_spaces,
            'opponents_taken_pieces': opponents_taken_pieces,
            'sum_distances': sum_distances,
            'sum_distances_opponent': sum_distances_opponent,
            'number_of_singles': number_of_singles,
            'sum_single_distance_away_from_home': sum_single_distance_away_from_home,
            'pieces_on_board': pieces_on_board,
            'sum_distances_to_endzone': sum_distances_to_endzone,
            'num_locations_with_two_or_three_pieces': num_locations_with_two_or_three_pieces
        }

    # Function that will start the process to determine the best move, then
    # move the piece
    def move(self, board, colour, dice_roll, make_move, opponents_activity):

        # Determine the best move available
        result = self.move_recursively(board, colour, dice_roll)
        # If the roll is a double then the length will be 4
        not_a_double = len(dice_roll) == 2
        # If the roll is not a double then also check the dice in the reverse
        # order to ensure we currently have chosen the best possible move
        if not_a_double:
            new_dice_roll = dice_roll.copy()
            new_dice_roll.reverse()
            result_swapped = self.move_recursively(board, colour,
                                                   dice_rolls=new_dice_roll)
            if result_swapped['best_value'] < result['best_value'] and \
                    len(result_swapped['best_moves']) >= len(result['best_moves']):
                result = result_swapped

        # Make the best move(s)
        if len(result['best_moves']) != 0:
            for move in result['best_moves']:
                make_move(move['piece_at'], move['die_roll'])

    # Function that will recursively check for the best move
    def move_recursively(self, board, colour, dice_rolls):
        best_board_value = float('inf')
        best_pieces_to_move = []

        # Get the players current pieces
        pieces_to_try = [x.location for x in board.get_pieces(colour)]
        pieces_to_try = list(set(pieces_to_try))

        # Get one piece from each location to test
        valid_pieces = []
        for piece_location in pieces_to_try:
            valid_pieces.append(board.get_piece_at(piece_location))
        valid_pieces.sort(key=Piece.spaces_to_home, reverse=True)

        # Get the first dice roll
        dice_rolls_left = dice_rolls.copy()
        die_roll = dice_rolls_left.pop(0)

        # Iterate through each piece and test possible moves
        for piece in valid_pieces:
            if board.is_move_possible(piece, die_roll):
                board_copy = board.create_copy()
                new_piece = board_copy.get_piece_at(piece.location)
                board_copy.move_piece(new_piece, die_roll)
                if len(dice_rolls_left) > 0:
                    result = self.move_recursively(board_copy, colour, dice_rolls_left)
                    if len(result['best_moves']) == 0:
                        # we have done the best we can do
                        board_value = self.evaluate_board(board_copy, colour)
                        if board_value < best_board_value and len(best_pieces_to_move) < 2:
                            best_board_value = board_value
                            best_pieces_to_move = [{'die_roll': die_roll, 'piece_at': piece.location}]
                    elif result['best_value'] < best_board_value:
                        new_best_moves_length = len(result['best_moves']) + 1
                        if new_best_moves_length >= len(best_pieces_to_move):
                            best_board_value = result['best_value']
                            move = {'die_roll': die_roll, 'piece_at': piece.location}
                            best_pieces_to_move = [move] + result['best_moves']
                else:
                    board_value = self.evaluate_board(board_copy, colour)
                    if board_value < best_board_value and len(best_pieces_to_move) < 2:
                        best_board_value = board_value
                        best_pieces_to_move = [{'die_roll': die_roll, 'piece_at': piece.location}]

        return {'best_value': best_board_value,
                'best_moves': best_pieces_to_move}


class CompareAllMovesSimple(CompareAllMoves):

    def evaluate_board(self, myboard, colour):
        board_stats = self.assess_board(colour, myboard)

        board_value = board_stats['sum_distances'] + 2 * board_stats['number_of_singles'] - \
                      board_stats['number_occupied_spaces'] - board_stats['opponents_taken_pieces']
        return board_value


class CompareAllMovesWeightingDistance(CompareAllMoves):

    def evaluate_board(self, myboard, colour):
        board_stats = self.assess_board(colour, myboard)
        board_value = board_stats['sum_distances'] - float(board_stats['sum_distances_opponent'])/3 + \
                      2 * board_stats['number_of_singles'] - \
                      board_stats['number_occupied_spaces'] - board_stats['opponents_taken_pieces']
        return board_value


class CompareAllMovesWeightingDistanceAndSingles(CompareAllMoves):

    def evaluate_board(self, myboard, colour):
        board_stats = self.assess_board(colour, myboard)

        board_value = board_stats['sum_distances'] - float(board_stats['sum_distances_opponent'])/3 + \
                      float(board_stats['sum_single_distance_away_from_home'])/6 - \
                      board_stats['number_occupied_spaces'] - board_stats['opponents_taken_pieces']
        return board_value


class CompareAllMovesWeightingDistanceAndSinglesWithEndGame(CompareAllMoves):

    def evaluate_board(self, myboard, colour):
        board_stats = self.assess_board(colour, myboard)

        board_value = board_stats['sum_distances'] - float(board_stats['sum_distances_opponent']) / 3 + \
                      float(board_stats['sum_single_distance_away_from_home']) / 6 - \
                      board_stats['number_occupied_spaces'] - board_stats['opponents_taken_pieces'] + \
                      3 * board_stats['pieces_on_board']

        return board_value


class CompareAllMovesWeightingDistanceAndSinglesWithEndGame2(CompareAllMoves):

    def evaluate_board(self, myboard, colour):
        board_stats = self.assess_board(colour, myboard)

        board_value = board_stats['sum_distances'] - float(board_stats['sum_distances_opponent']) / 3 + \
                      float(board_stats['sum_single_distance_away_from_home']) / 6 - \
                      board_stats['number_occupied_spaces'] - board_stats['opponents_taken_pieces'] + \
                      3 * board_stats['pieces_on_board'] + float(board_stats['sum_distances_to_endzone']) / 6

        return board_value

