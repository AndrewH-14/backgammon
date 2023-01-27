import os
import threading
import sys

# Get the program ID, start idx, and end idx
prog_id   = sys.argv[1]
start_idx = int(sys.argv[2])
end_idx   = int(sys.argv[3])

# Read in the potential weight combinations to be tested
weight_combination_file = open("combinations.txt", "r")
weight_combination_string = weight_combination_file.read()
weight_combination_list = weight_combination_string.split("\n")
weight_combination_list_len = len(weight_combination_list)

# Create the thread class and give it a start and end index for the combination file.
class thread(threading.Thread):
    start_idx = 0
    end_idx = 0
    num_games = 0
    def __init__(self, thread_name, thread_ID, start_idx, end_idx, num_games):
        threading.Thread.__init__(self)
        self.thread_name = thread_name
        self.thread_ID = thread_ID
        self.start_idx = start_idx
        self.end_idx = end_idx
        self.num_games = num_games

    def run(self):
        # Print off the threads name and ID
        # print(str(self.thread_name) +" "+ str(self.thread_ID))
        # Store the output file name
        output_file_name = self.thread_name + "-" + prog_id + ".txt"
        # Store the results file name
        results_file_name = self.thread_name + "-results-" + prog_id + ".txt"
        final_file = open(results_file_name, "w")
        # Win count variables
        white_win_count = 0
        # Iterate through the lines that this thread is responsible for
        for idx in range(self.start_idx, self.end_idx + 1):
            # Deletes the output.txt file contents
            file_to_delete = open(output_file_name,'w')
            file_to_delete.close()
            # Run the desired number of games and check the win percentage
            for game_idx in range(0, self.num_games):
                # If the win percentage is less than 30 percent halfway through
                # the weight test, move on to the next weight
                if game_idx == (self.num_games // 2):
                    results_file = open(output_file_name, "r")
                    file_contents = results_file.read()
                    white_win_count = file_contents.count("wh")
                    results_file.close()
                    win_percentage = white_win_count / self.num_games
                    if win_percentage < 0.20:
                        break

                # If the win percentage is less than 40 through 3/4 through the
                # weight test, move on to the next weight
                if game_idx == ((self.num_games * 3) // 4):
                    results_file = open(output_file_name, "r")
                    file_contents = results_file.read()
                    white_win_count = file_contents.count("wh")
                    results_file.close()
                    win_percentage = white_win_count / self.num_games
                    if win_percentage < 0.20:
                        break

                # Remove the brackets from the line
                line = weight_combination_list[idx].replace("[", "")
                line = line.replace("]", "")
                line = line.replace(" ", "")

                # Run the backgammon game and output results to the output file
                os.system('python3 ../auto.py               \
                           player1_achankins                \
                           CompareAllMovesWeightingDistance \
                           false '                          \
                           + line +                         \
                           ' >> ' + output_file_name)

            # Get the final win percentage
            results_file    = open(output_file_name, "r")
            file_contents   = results_file.read()
            white_win_count = file_contents.count("wh")
            win_percentage  = white_win_count / self.num_games
            results_file.close()

            # If the current weight has a win percentage over 50 record it
            if (win_percentage > 0.20):
                final_file.write(line + str(win_percentage))

        final_file.close()


# Initialize the threads

thread1 = thread("thread1", 1, start_idx, (start_idx + (end_idx - start_idx) // 2), 100)
thread2 = thread("thread2", 2, (start_idx + (end_idx - start_idx) // 2) + 1, end_idx, 100)
# thread3 = thread("thread3", 3, (list_section_len * 2) + 1, (list_section_len * 3), 100)
# thread4 = thread("thread4", 4, (list_section_len * 3) + 1, (list_section_len * 4), 100)
# thread5 = thread("thread5", 5, (list_section_len * 4) + 1, (list_section_len * 5), 100)

# Run the threads
thread1.start()
thread2.start()
