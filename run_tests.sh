#!/bin/bash

# Delete any previous output
truncate -s 0 output.txt

# Run the game 100 times and save the output to a text file
for i in {1..100}
do
    python3 auto.py player1_achankins CompareAllMovesWeightingDistance false >> output.txt
done

# Use grep to comput win percentages
echo "player1_achankins win count:"
echo $(grep "white won" output.txt | wc -l)
echo "CompareAllMovesWeightingDistance win count:"
echo $(grep "black won" output.txt | wc -l)
