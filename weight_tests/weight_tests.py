import os
import threading

weight_combination_file = open("combinations.txt", "r")
weight_combination_string = weight_combination_file.read()
weight_combination_list = weight_combination_string.split("\n")
weight_combination_list_len = len(weight_combination_list)

# Create the thread class and give it a start and end index for the combination file.
class thread(threading.Thread):
    start_idx = 0
    end_idx = 0
    def __init__(self, thread_name, thread_ID, start_idx, end_idx):
        threading.Thread.__init__(self)
        self.thread_name = thread_name
        self.thread_ID = thread_ID
        self.start_idx = start_idx
        self.end_idx

        # helper function to execute the threads
    def run(self):
        print(str(self.thread_name) +" "+ str(self.thread_ID))


# Number of games to run for each weight value
num_games = 50
# Best win percentage and weight
best_win_percentage = 0.0
# Win count variables
white_win_count = 0

# Delete all previous test output
# Deletes the output.txt file contents
file_to_delete = open("best_result",'w')
file_to_delete.close()
file_to_delete = open("weights.txt",'w')
file_to_delete.close()



# Initialize the threads
list_section_len = weight_combination_list_len // 5
thread1 = thread("thread1", 1, 0, list_section_len)
thread2 = thread("thread2", 2, list_section_len + 1, (list_section_len * 2))
thread3 = thread("thread3", 3, (list_section_len * 2) + 1, (list_section_len * 3))
thread4 = thread("thread4", 4, (list_section_len * 3) + 1, (list_section_len * 4))
thread5 = thread("thread5", 5, (list_section_len * 4) + 1, (list_section_len * 5))

# Run

with open("combinations.txt", "r") as combination_file:
    for line in combination_file:
        # Deletes the output.txt file contents
        file_to_delete = open("output.txt",'w')
        file_to_delete.close()
        # Run the desired number of games and check the win percentage at the end
        for idx in range(0, num_games):
            # If the win percentage is less than 30 halfway through the weight test,
            # move on to the next weight
            if idx == num_games // 2:
                results_file    = open("output.txt", "r")
                file_contents   = results_file.read()
                white_win_count = file_contents.count("white won")
                results_file.close()
                win_percentage  = white_win_count / num_games
                if win_percentage < 0.30:
                    break

            # If the win percentage is less than 40 3/4 through the weight test,
            # move on to the next weight
            if idx == ((num_games * 3) // 4):
                results_file    = open("output.txt", "r")
                file_contents   = results_file.read()
                white_win_count = file_contents.count("white won")
                results_file.close()
                win_percentage  = white_win_count / num_games
                if win_percentage < 0.40:
                    break

            # Remove the brackets from the line
            line = line.replace("[", "")
            line = line.replace("]", "")

            # Write the weight to be used to the weights.txt file so that the
            # backgammon program can access it
            weight_file = open("weights.txt", 'w')
            weight_file.write(line)
            weight_file.close()

            # Run the backgammon game and output results to the output file
            os.system('python3 ../auto.py               \
                       player1_achankins                \
                       CompareAllMovesWeightingDistance \
                       false                            \
                       >> output.txt')

        # Get the final win percentage
        results_file    = open("output.txt", "r")
        file_contents   = results_file.read()
        white_win_count = file_contents.count("white won")
        win_percentage  = white_win_count / num_games
        results_file.close()

        # If the current weight has the best win percentage then store it and the
        # win percentage in the file
        if (win_percentage > best_win_percentage):
            best_win_percentage = win_percentage
            best_weight = line
            best_result_file = open("best_result.txt", "w")
            best_result_file.write(best_weight + str(best_win_percentage))
            best_result_file.close()
