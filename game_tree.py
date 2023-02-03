import copy

"""
Finds the possible moves that white has if the given roll is used. Will return
a list of pairs [<current position>, <new position>]
"""
def find_possible_moves(player_to_move, player_not_moving, roll, direction):
    copy_player_to_move = copy.deepcopy(player_to_move)
    copy_player_not_moving = copy.deepcopy(player_not_moving)
    # Check if we have a piece off the board that must be added back
    if copy_player_to_move[0][0] != 0:
        # Check if there are any moves possible
        if direction == "ascending":
            if copy_player_not_moving[1][roll - 1] > 1:
                # No moves possible return an empty list of lists
                return [[]]
            else:
                # One move possible return where the white piece must be placed
                return [[roll - 1]]
        else:
            if copy_player_not_moving[copy_player_not_moving[1][24 - roll - 1]]:
                return [[]]
            else:
                return[[24 - roll - 1]]

    # Check any other possible moves
    possible_moves = []
    for location_idx in range(len(copy_player_to_move[1])):
        # Check to see if there is a white piece at the location
        if copy_player_to_move[1][location_idx] > 0:
            if direction == "ascending":
                # Check to see if we can move the piece with the dice roll
                if location_idx + roll < 24 and copy_player_not_moving[1][location_idx + roll] <= 1:
                    # We can move this piece so add it to the possible moves list
                    possible_moves.append([location_idx, location_idx + roll])
            else:
                if location_idx - roll >= 0 and copy_player_not_moving[1][location_idx - roll] <= 1:
                    possible_moves.append([location_idx, location_idx - roll])

    return possible_moves

# Determines if two boards are exactly the same of not
def compare_boards(board1, board2):
    # First compare the taken and home pieces
    if board1[0][0][0] != board2[0][0][0]:
        return False
    if board1[0][2][0] != board2[0][2][0]:
        return False
    if board1[1][0][0] != board2[1][0][0]:
        return False
    if board1[1][2][0] != board2[1][2][0]:
        return False
    # Next compare the white pieces
    for idx in range(0, 24):
        if board1[0][1][idx] != board2[0][1][idx]:
            return False
    # Next compare the white pieces
    for idx in range(0, 24):
        if board1[1][1][idx] != board2[1][1][idx]:
            return False
    # Boards are equal
    return True

# Will remove duplicate boards from the list and return the result
def remove_duplicates(list_of_boards):
    # Remove any duplicate states
    boards_after_duplicates_removed = []
    for board1 in list_of_boards:
        add_to_list = True
        for board2 in boards_after_duplicates_removed:
            if compare_boards(board1, board2):
                add_to_list = False
        if add_to_list:
            boards_after_duplicates_removed.append(board1)
    return boards_after_duplicates_removed

"""
Function that will make all the moves given and return the resulting boards.
"""
def make_possible_moves(player1, player2, possible_moves, previous_move):
    # Generate all the new states using the roll of five
    new_states_after_first_move = []
    for idx in range(len(possible_moves)):
        new_player1 = copy.deepcopy(player1)
        new_player2 = copy.deepcopy(player2)
        # Do the move that was returned
        move_to_make = possible_moves[idx]
        # Determine what type of move it was
        if len(move_to_make) == 1:
            # The move just added a piece to the board
            # Add remove the piece from the taken pile
            new_player1[0][0] = player1[0][0] - 1
            # Add the piece to the board
            new_player2[1][move_to_make[0]] = player1[1][move_to_make[0]] + 1
            # Remove a black piece if necessary
            if player2[1][move_to_make[0]] == 1:
                # Remove the black piece
                new_player2[1][move_to_make[0]] = 0
                # Add it to the taken pile
                new_player2[0][0] = player2[0][0] + 1
        elif move_to_make[1] != 24:
            # Moving a piece on the board to another location on the board
            # Remove the piece from its current location
            new_player1[1][move_to_make[0]] = player1[1][move_to_make[0]] - 1
            # Add the piece to its new location
            new_player1[1][move_to_make[1]] = player1[1][move_to_make[1]] + 1
            # Remove a black piece if necessary
            if state_black[1][move_to_make[1]] == 1:
                # Remove the black piece
                new_player2[1][move_to_make[1]] = 0
                # Add it to the taken pile
                new_player2[0][0] = player2[0][0] + 1
        else:
            # Moving a piece off of the board
            # Remove the piece from its current location
            new_player2[1][move_to_make[0]] = player1[1][move_to_make[0]] - 1
            # Add the piece to the home location
            new_player1[2][0] = player1[2][0] + 1

        # Append the new state to the list
        if previous_move is None:
            new_state = [new_player1, new_player2, move_to_make]
            new_states_after_first_move.append(new_state)
        else:
            new_state = [new_player1, new_player2, previous_move, move_to_make]
            new_states_after_first_move.append(new_state)
    return new_states_after_first_move
"""
Player 1 is the player who is currently making a move
Player 2 is the player who player 1 is playing against
"""
def get_new_boards_helper(player1, player2, roll, direction):
    # Start of options after the pick for 5 has been made 1
    possible_moves = find_possible_moves(player1, player2, roll[0], direction)
    # Generate all the new states using the roll of five
    new_states_after_first_move = make_possible_moves(player1, player2, possible_moves, None)

    # Store the moves that were made
    moves_mades = []
    for state in new_states_after_first_move:
        moves_mades.append(state[2])

    # Find options for the second move
    states_after_both_moves = []
    for idx in range(0, len(new_states_after_first_move)):
        possible_moves = find_possible_moves(new_states_after_first_move[idx][0], new_states_after_first_move[idx][1], roll[1], direction)
        states_after_both_moves = states_after_both_moves + make_possible_moves(new_states_after_first_move[idx][0], new_states_after_first_move[idx][1], possible_moves, moves_mades[idx])

    return remove_duplicates(states_after_both_moves)

"""
Will get all of the resulting boards from the using the given dice roll.
Player 1 is the player who is making their move
Player 2 is the opposing player
"""
def get_new_boards(player1, player2, roll, direction):
    new_boards1 = get_new_boards_helper(player1, player2, [roll[0], roll[1]], direction)
    new_boards2 = get_new_boards_helper(player1, player2, [roll[1], roll[0]], direction)
    new_boards = new_boards1 + new_boards2
    return remove_duplicates(new_boards)


"""
Function that will evaluate a board and return its value based on the formula
used in the CompareAllMovesWeightingDistance
"""
def evaluate_board(player1, player2):
    # First we need to compute all of the features that are used
    # Compute 'sum_distances' (sum of all pieces distance to the end)
    sum_distances = 0
    for idx in range(len(player1[1])):
        # Multiply the distance to home by the number of pieces at that location
        sum_distances += (24 - idx) * player1[1][idx]
    # Compute 'sum_distances_opponent'
    sum_distances_opponent = 0
    for idx in range(len(player2[1])):
        # Multiply the distance to home by the number of pieces at that location
        sum_distances_opponent += (idx + 1) * player2[1][idx]
    # Compute 'number_of_singles'
    num_singles = 0
    for idx in range(len(player1[1])):
        # If there is only a single piece at the location add it
        if player1[1][idx] == 1:
            num_singles += 1
    # Compute 'number_of_occupied_spaces'
    num_occupied_spaces = 0
    for idx in range(len(player1[1])):
        if player1[1][idx] > 1:
            num_occupied_spaces += 1
    # Compute 'opponents_taken_pieces'
    opponents_taken_pieces = player2[0][0]
    # Caculate the value
    board_value = sum_distances - \
                  (float(sum_distances_opponent) / 3) + \
                  (2 * num_singles) - \
                  num_occupied_spaces - \
                  opponents_taken_pieces
    return board_value

"""
Function that will take a move string based on the board 0...23 and convert it to
a string of the board 1...24
"""
def convert_move(move):
    return str([move[0] + 1, move[1] + 1])

# [[<pieces off board>], [<pieces on board (position 0-23)>]]
state_white = [[0], [0, 1, 0, 0, 2, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 2, 0, 6, 0, 0, 0, 0, 0], [0]]
state_black = [[0], [0, 0, 2, 0, 0, 6, 0, 0, 0, 0, 0, 0, 4, 0, 1, 0, 0, 0, 0, 0, 0, 2, 0, 0], [0]]

# The boards and moves after player1 has rolled [5, 2]
new_boards = get_new_boards(state_white, state_black, [5, 2], "ascending")
print("Initial State:")
print("Roll: [5,2]")
for idx in range(len(new_boards)):
    print("State " + str(idx + 1) + ": " + convert_move(new_boards[idx][2]) + " " + convert_move(new_boards[idx][3]) + " " + str(evaluate_board(new_boards[idx][0], new_boards[idx][1])))
print("")

# For each board, the opponent can either roll a [1,6], [3,5], [2, 3], [1,2]
for idx in range(len(new_boards)):
    # THe boards and moves after player1 has rolled a [1,6]
    # Black will now be at index 0 of new_boards1
    new_boards1 = get_new_boards(new_boards[idx][1], new_boards[idx][0], [1,6], "descending")
    print("Previous State: " + str(idx + 1))
    print("Roll: [1,6]")
    for idx1 in range(len(new_boards1)):
        print("State " + str(idx1 + 1) + ": " + convert_move(new_boards1[idx1][2]) + " " + convert_move(new_boards1[idx1][3]) + " " + str(evaluate_board(new_boards1[idx1][0], new_boards1[idx1][1])))
    print("")

    # The boards and moves after player1 has rolled a [3,5]
    new_boards2 = get_new_boards(new_boards[idx][1], new_boards[idx][0], [3,5], "descending")
    print("Previous State: " + str(idx + 1))
    print("Roll: [3,5]")
    for idx2 in range(len(new_boards2)):
        print("State " + str(idx2 + 1) + ": " + convert_move(new_boards2[idx2][2]) + " " + convert_move(new_boards2[idx2][3]) + " " + str(evaluate_board(new_boards2[idx2][0], new_boards2[idx2][1])))
    print("")

    # The boards and moves after player1 has rolled a [2,3]
    new_boards3 = get_new_boards(new_boards[idx][1], new_boards[idx][0], [2,3], "descending")
    print("Previous State: " + str(idx + 1))
    print("Roll: [2,3]")
    for idx3 in range(len(new_boards3)):
        print("State " + str(idx3 + 1) + ": " + convert_move(new_boards3[idx3][2]) + " " + convert_move(new_boards3[idx3][3]) + " " + str(evaluate_board(new_boards3[idx3][0], new_boards3[idx3][1])))
    print("")

    # The boards and moves after player1 has rolled a [1,2]
    new_boards4 = get_new_boards(new_boards[idx][1], new_boards[idx][0], [1,2], "descending")
    print("Previous State: " + str(idx + 1))
    print("Roll: [1,2]")
    for idx4 in range(len(new_boards4)):
        print("State " + str(idx4 + 1) + ": " + convert_move(new_boards4[idx4][2]) + " " + convert_move(new_boards4[idx4][3]) + " " + str(evaluate_board(new_boards4[idx4][0], new_boards4[idx4][1])))
    print("")