import copy

"""
Finds the possible moves that white has if the given roll is used. Will return
a list of pairs [<current position>, <new position>]
"""
def find_possible_moves(state_white, state_black, roll):
    copy_state_white = copy.deepcopy(state_white)
    copy_state_black = copy.deepcopy(state_black)
    # Check if we have a piece off the board that must be added back
    if copy_state_white[0][0] != 0:
        # Check if there are any moves possible
        if copy_state_black[1][roll - 1] > 1:
            # No moves possible return an empty list of lists
            return [[]]
        else:
            # One move possible return where the white piece must be placed
            return [[roll - 1]]

    # Check any other possible moves
    possible_moves = []
    for location_idx in range(len(copy_state_white[1])):
        # Check to see if their is a white piece at the location
        if copy_state_white[1][location_idx] > 0:
            # Check to see if we can move the piece with the dice roll
            if (location_idx + roll) > 23:
                # Piece has made it home
                possible_moves.append([location_idx, 24])
            elif copy_state_black[1][location_idx + roll] <= 1:
                # We can move this piece so add it to the possible moves list
                possible_moves.append([location_idx, location_idx + roll])

    return possible_moves

def get_new_states(state_white, state_black, roll):
    # Start of options after the pick for 5 has been made 1
    possible_moves = find_possible_moves(state_white, state_black, roll)

    # Generate all the new states using the roll of five
    new_states = []
    for idx in range(len(possible_moves)):
        new_state_white = copy.deepcopy(state_white)
        new_state_black = copy.deepcopy(state_black)
        # Do the move that was returned
        move_to_make = possible_moves[idx]
        # Determine what type of move it was
        if len(move_to_make) == 1:
            # The move just added a piece to the board
            # Add remove the piece from the taken pile
            new_state_white[0][0] = state_white[0][0] - 1
            # Add the piece to the board
            new_state_white[1][move_to_make[0]] = state_white[1][move_to_make[0]] + 1
            # Remove a black piece if necessary
            if state_black[1][move_to_make[0]] == 1:
                # Remove the black piece
                new_state_black[1][move_to_make[0]] = 0
                # Add it to the taken pile
                new_state_black[0][0] = state_black[0][0] + 1
        elif move_to_make[1] != 24:
            # Moving a piece on the board to another location on the board
            # Remove the piece from its current location
            new_state_white[1][move_to_make[0]] = state_white[1][move_to_make[0]] - 1
            # Add the piece to its new location
            new_state_white[1][move_to_make[1]] = state_white[1][move_to_make[1]] + 1
            # Remove a black piece if necessary
            if state_black[1][move_to_make[1]] == 1:
                # Remove the black piece
                new_state_black[1][move_to_make[1]] = 0
                # Add it to the taken pile
                new_state_black[0][0] = state_black[0][0] + 1
        else:
            # Moving a piece off of the board
            # Remove the piece from its current location
            new_state_white[1][move_to_make[0]] = state_white[1][move_to_make[0]] - 1
            # Add the piece to the home location
            new_state_white[2][0] = state_white[2][0] + 1

        # Append the new state to the list
        new_state = [new_state_white, new_state_black]
        new_states.append(new_state)

    return new_states

"""
Function that will evaluate a board and return its value based on the formula
used in the CompareAllMovesWeightingDistance
"""
def evaluate_board(state_white, state_black):
    # First we need to compute all of the features that are used
    # Compute 'sum_distances' (sum of all pieces distance to the end)
    sum_distances = 0
    for idx in range(len(state_white[1])):
        # Multiply the distance to home by the number of pieces at that location
        sum_distances += (24 - idx) * state_white[1][idx]
    # Compute 'sum_distances_opponent'
    sum_distances_opponent = 0
    for idx in range(len(state_black[1])):
        # Multiply the distance to home by the number of pieces at that location
        sum_distances_opponent += (idx + 1) * state_black[1][idx]
    # Compute 'number_of_singles'
    num_singles = 0
    for idx in range(len(state_white[1])):
        # If there is only a single piece at the location add it
        if state_white[1][idx] == 1:
            num_singles += 1
    # Compute 'number_of_occupied_spaces'
    num_occupied_spaces = 0
    for idx in range(len(state_white[1])):
        if state_white[1][idx] > 1:
            num_occupied_spaces += 1
    # Compute 'opponents_taken_pieces'
    opponents_taken_pieces = state_black[0][0]
    # Caculate the value
    board_value = sum_distances - \
                  (float(sum_distances_opponent) / 3) + \
                  (2 * num_singles) - \
                  num_occupied_spaces - \
                  opponents_taken_pieces
    print(sum_distances)
    print(sum_distances_opponent)
    print(num_singles)
    print(num_occupied_spaces)
    print(opponents_taken_pieces)
    return board_value

# [[<pieces off board>], [<pieces on board (position 0-23)>]]
state_white = [[0], [0, 1, 0, 0, 2, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 2, 0, 6, 0, 0, 0, 0, 0], [0]]
state_black = [[0], [0, 0, 2, 0, 0, 6, 0, 0, 0, 0, 0, 0, 4, 0, 1, 0, 0, 0, 0, 0, 0, 2, 0, 0], [0]]

# Generate all the new states using the roll of five
states_after_init_five = get_new_states(state_white, state_black, 5)

# Start of options after the pick for 5 has been made 1
states_after_init_five_zero = get_new_states(states_after_init_five[0][0], states_after_init_five[0][1], 2)
# Start of options after the pick for 5 has been made 1
states_after_init_five_one = get_new_states(states_after_init_five[1][0], states_after_init_five[1][1], 2)
# Start of options after the pick for 5 has been made 1
states_after_init_five_two = get_new_states(states_after_init_five[2][0], states_after_init_five[2][1], 2)
# Start of options after the pick for 5 has been made 1
states_after_init_five_three = get_new_states(states_after_init_five[3][0], states_after_init_five[3][1], 2)

# Generate all the new states using the roll of five
states_after_init_two = get_new_states(state_white, state_black, 2)

# Start of options after the pick for 5 has been made 1
states_after_init_two_zero = get_new_states(states_after_init_two[0][0], states_after_init_two[0][1], 5)
# Start of options after the pick for 5 has been made 1
states_after_init_two_one = get_new_states(states_after_init_two[1][0], states_after_init_two[1][1], 5)
# Start of options after the pick for 5 has been made 1
states_after_init_two_two = get_new_states(states_after_init_two[2][0], states_after_init_two[2][1], 5)
# Start of options after the pick for 5 has been made 1
states_after_init_two_three = get_new_states(states_after_init_two[3][0], states_after_init_two[3][1], 5)
# Start of options after the pick for 5 has been made 1
states_after_init_two_four = get_new_states(states_after_init_two[3][0], states_after_init_two[3][1], 5)


def pieces_at_text(state_white, state_black, location):
    if state_white[1][location] == 0 and state_black[1][location] == 0:
        return " .  "
    if state_white[1][location] > 0:
        return " %sW " % (state_white[1][location])
    else:
        return " %sB " % (state_black[1][location])

def print_board(state_white, state_black):
    print("  12                  17   18                  23")
    print("---------------------------------------------------")
    line = "|"
    for i in range(12, 17 + 1):
        line = line + pieces_at_text(state_white, state_black, i)
    line = line + "|"
    for i in range(18, 23 + 1):
        line = line + pieces_at_text(state_white, state_black, i)
    line = line + "|"
    print(line)
    for _ in range(3):
        print("|                        |                        |")
    line = "|"
    for i in reversed(range(6, 11+1)):
        line = line + pieces_at_text(state_white, state_black, i)
    line = line + "|"
    for i in reversed(range(0, 5+1)):
        line = line + pieces_at_text(state_white, state_black, i)
    line = line + "|"
    print(line)
    print("---------------------------------------------------")
    print("  11                  6    5                   0")

board_id = 1

# Print out first level of the game tree
print("Initial Board State:")
print("Board ID: " + str(board_id))
print("Rolls left: [5, 2]")
print("White's taken pieces: " + str(state_white[0][0]) + " | White's completed pieces: " + str(state_white[2][0]))
print("Black's taken pieces: " + str(state_black[0][0]) + " | Black's completed pieces: " + str(state_black[2][0]))
print("Board's value: " + str(evaluate_board(state_white, state_black)))
print_board(state_white, state_black)
print("\n")
board_id += 1

# Print out the second level of the state tree
for idx in range(len(states_after_init_five)):
    state_white = states_after_init_five[idx][0]
    state_black = states_after_init_five[idx][1]
    print("First Move Board State:")
    print("Board ID: " + str(board_id))
    print("Parent Board ID: 1")
    print("Rolls left: [2]")
    print("White's taken pieces: " + str(state_white[0][0]) + " | White's completed pieces: " + str(state_white[2][0]))
    print("Black's taken pieces: " + str(state_black[0][0]) + " | Black's completed pieces: " + str(state_black[2][0]))
    print("Board's value: " + str(evaluate_board(state_white, state_black)))
    print_board(state_white, state_black)
    print("\n")
    board_id += 1

# Print out the second level of the state tree
for idx in range(len(states_after_init_two)):
    state_white = states_after_init_two[idx][0]
    state_black = states_after_init_two[idx][1]
    print("First Move Board State:")
    print("Board ID: " + str(board_id))
    print("Parent Board ID: 1")
    print("Rolls left: [5]")
    print("White's taken pieces: " + str(state_white[0][0]) + " | White's completed pieces: " + str(state_white[2][0]))
    print("Black's taken pieces: " + str(state_black[0][0]) + " | Black's completed pieces: " + str(state_black[2][0]))
    print("Board's value: " + str(evaluate_board(state_white, state_black)))
    print_board(state_white, state_black)
    print("\n")
    board_id += 1

# Print out the second level of the state tree
for idx in range(len(states_after_init_five_zero)):
    state_white = states_after_init_five_zero[idx][0]
    state_black = states_after_init_five_zero[idx][1]
    print("Second Move Board State:")
    print("Board ID: " + str(board_id))
    print("Parent Board ID: 2")
    print("Rolls left: []")
    print("White's taken pieces: " + str(state_white[0][0]) + " | White's completed pieces: " + str(state_white[2][0]))
    print("Black's taken pieces: " + str(state_black[0][0]) + " | Black's completed pieces: " + str(state_black[2][0]))
    print("Board's value: " + str(evaluate_board(state_white, state_black)))
    print_board(state_white, state_black)
    print("\n")
    board_id += 1

# Print out the second level of the state tree
for idx in range(len(states_after_init_five_one)):
    state_white = states_after_init_five_one[idx][0]
    state_black = states_after_init_five_one[idx][1]
    print("Second Move Board State:")
    print("Board ID: " + str(board_id))
    print("Parent Board ID: 3")
    print("Rolls left: []")
    print("White's taken pieces: " + str(state_white[0][0]) + " | White's completed pieces: " + str(state_white[2][0]))
    print("Black's taken pieces: " + str(state_black[0][0]) + " | Black's completed pieces: " + str(state_black[2][0]))
    print("Board's value: " + str(evaluate_board(state_white, state_black)))
    print_board(state_white, state_black)
    print("\n")
    board_id += 1

# Print out the second level of the state tree
for idx in range(len(states_after_init_five_two)):
    state_white = states_after_init_five_two[idx][0]
    state_black = states_after_init_five_two[idx][1]
    print("Second Move Board State:")
    print("Board ID: " + str(board_id))
    print("Parent Board ID: 4")
    print("Rolls left: []")
    print("White's taken pieces: " + str(state_white[0][0]) + " | White's completed pieces: " + str(state_white[2][0]))
    print("Black's taken pieces: " + str(state_black[0][0]) + " | Black's completed pieces: " + str(state_black[2][0]))
    print("Board's value: " + str(evaluate_board(state_white, state_black)))
    print_board(state_white, state_black)
    print("\n")
    board_id += 1

# Print out the second level of the state tree
for idx in range(len(states_after_init_five_three)):
    state_white = states_after_init_five_three[idx][0]
    state_black = states_after_init_five_three[idx][1]
    print("Second Move Board State:")
    print("Board ID: " + str(board_id))
    print("Parent Board ID: 5")
    print("Rolls left: []")
    print("White's taken pieces: " + str(state_white[0][0]) + " | White's completed pieces: " + str(state_white[2][0]))
    print("Black's taken pieces: " + str(state_black[0][0]) + " | Black's completed pieces: " + str(state_black[2][0]))
    print("Board's value: " + str(evaluate_board(state_white, state_black)))
    print_board(state_white, state_black)
    print("\n")
    board_id += 1

# Print out the second level of the state tree
for idx in range(len(states_after_init_two_zero)):
    state_white = states_after_init_two_zero[idx][0]
    state_black = states_after_init_two_zero[idx][1]
    print("Second Move Board State:")
    print("Board ID: " + str(board_id))
    print("Parent Board ID: 6")
    print("Rolls left: []")
    print("White's taken pieces: " + str(state_white[0][0]) + " | White's completed pieces: " + str(state_white[2][0]))
    print("Black's taken pieces: " + str(state_black[0][0]) + " | Black's completed pieces: " + str(state_black[2][0]))
    print("Board's value: " + str(evaluate_board(state_white, state_black)))
    print_board(state_white, state_black)
    print("\n")
    board_id += 1

# Print out the second level of the state tree
for idx in range(len(states_after_init_two_one)):
    state_white = states_after_init_two_one[idx][0]
    state_black = states_after_init_two_one[idx][1]
    print("Second Move Board State:")
    print("Board ID: " + str(board_id))
    print("Parent Board ID: 7")
    print("Rolls left: []")
    print("White's taken pieces: " + str(state_white[0][0]) + " | White's completed pieces: " + str(state_white[2][0]))
    print("Black's taken pieces: " + str(state_black[0][0]) + " | Black's completed pieces: " + str(state_black[2][0]))
    print("Board's value: " + str(evaluate_board(state_white, state_black)))
    print_board(state_white, state_black)
    print("\n")
    board_id += 1

# Print out the second level of the state tree
for idx in range(len(states_after_init_two_two)):
    state_white = states_after_init_two_two[idx][0]
    state_black = states_after_init_two_two[idx][1]
    print("Second Move Board State:")
    print("Board ID: " + str(board_id))
    print("Parent Board ID: 8")
    print("Rolls left: []")
    print("White's taken pieces: " + str(state_white[0][0]) + " | White's completed pieces: " + str(state_white[2][0]))
    print("Black's taken pieces: " + str(state_black[0][0]) + " | Black's completed pieces: " + str(state_black[2][0]))
    print("Board's value: " + str(evaluate_board(state_white, state_black)))
    print_board(state_white, state_black)
    print("\n")
    board_id += 1

# Print out the second level of the state tree
for idx in range(len(states_after_init_two_three)):
    state_white = states_after_init_two_three[idx][0]
    state_black = states_after_init_two_three[idx][1]
    print("Second Move Board State:")
    print("Board ID: " + str(board_id))
    print("Parent Board ID: 9")
    print("Rolls left: []")
    print("White's taken pieces: " + str(state_white[0][0]) + " | White's completed pieces: " + str(state_white[2][0]))
    print("Black's taken pieces: " + str(state_black[0][0]) + " | Black's completed pieces: " + str(state_black[2][0]))
    print("Board's value: " + str(evaluate_board(state_white, state_black)))
    print_board(state_white, state_black)
    print("\n")
    board_id += 1

# Print out the second level of the state tree
for idx in range(len(states_after_init_two_four)):
    state_white = states_after_init_two_four[idx][0]
    state_black = states_after_init_two_four[idx][1]
    print("Second Move Board State:")
    print("Board ID: " + str(board_id))
    print("Parent Board ID: 10")
    print("Rolls left: []")
    print("White's taken pieces: " + str(state_white[0][0]) + " | White's completed pieces: " + str(state_white[2][0]))
    print("Black's taken pieces: " + str(state_black[0][0]) + " | Black's completed pieces: " + str(state_black[2][0]))
    print("Board's value: " + str(evaluate_board(state_white, state_black)))
    print_board(state_white, state_black)
    print("\n")
    board_id += 1