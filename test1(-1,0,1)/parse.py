# Open the file where the resulting weights/win percentage will be stored
output_file = open("final_results.txt", "w")

# Parse the first file
file = open("thread1-results-0.txt", "r")
while True:

    # Get the candidate from the file
    weight = file.readline()

    if weight == "":
        break

    win_percentage = float(file.readline())

    if win_percentage > 0.5:
        output_file.write(weight)
file.close()

# Parse the second file
file = open("thread1-results-1.txt", "r")
while True:

    # Get the candidate from the file
    weight = file.readline()

    if weight == "":
        break

    win_percentage = float(file.readline())

    if win_percentage > 0.5:
        output_file.write(weight)
file.close()

# Parse the third file
file = open("thread1-results-2.txt", "r")
while True:

    # Get the candidate from the file
    weight = file.readline()

    if weight == "":
        break

    win_percentage = float(file.readline())

    if win_percentage > 0.5:
        output_file.write(weight)
file.close()

# Parse the fourth file
file = open("thread1-results-3.txt", "r")
while True:

    # Get the candidate from the file
    weight = file.readline()

    if weight == "":
        break

    win_percentage = float(file.readline())

    if win_percentage > 0.5:
        output_file.write(weight)
file.close()

# Parse the fifth file
file = open("thread1-results-4.txt", "r")
while True:

    # Get the candidate from the file
    weight = file.readline()

    if weight == "":
        break

    win_percentage = float(file.readline())

    if win_percentage > 0.5:
        output_file.write(weight)
file.close()

# Parse the sixth file
file = open("thread1-results-5.txt", "r")
while True:

    # Get the candidate from the file
    weight = file.readline()

    if weight == "":
        break

    win_percentage = float(file.readline())

    if win_percentage > 0.5:
        output_file.write(weight)
file.close()

# Close the outpout file
output_file.close()