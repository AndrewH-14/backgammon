from random import randint
import sys
from src.colour import Colour
from src.game import Game
from src.strategy_factory import StrategyFactory
from src.strategies import HumanStrategy
import numpy
import genetic_algorithm

import src.weight
import src.hash

import os
import threading
import sys

# Get the program ID, start idx, and end idx
# python3 auto.py <prog_id> <num_prog>
"""
prog_id_int = int(sys.argv[1])
prog_id_str = sys.argv[1]
num_prog    = int(sys.argv[2])
"""

# Generate weigths and store them in a list
"""
res = [[a, b, c, d, e, f, g, h, i] for a in [0.5, 0.75, 1.00]
                                   for b in [-0.5, -0.75, -1.0]
                                   for c in [-0.5, -0.75, -1.0]
                                   for d in [0.25, 0, -0.25]
                                   for e in [0.75, 1.0]
                                   for f in [0.75, 1.0]
                                   for g in [0]
                                   for h in [0.75, 1.0]
                                   for i in [0.25, 0.5, 0.75, 1.0]]
"""

# Get the weights from a file
# res = []
# combination_file = open("best_results.txt", "r")
# while True:
#     weight = combination_file.readline()
#     if weight == "":
#         break
#     weight = weight.replace("[", "")
#     weight = weight.replace("]", "")
#     weight_list = weight.split(",")
#     res.append([float(weight_list[0]), float(weight_list[1]), float(weight_list[2]), float(weight_list[3]),
#                 float(weight_list[4]), float(weight_list[5]), float(weight_list[6]), float(weight_list[7])])
# combination_file.close()

# res = [[0.75, -0.5, -1.0, -1, 1.0, 0.75, 0, 0.75, -0.1]]

# Compute the start and end index
"""
num_weights = len(res)
print(num_weights)
section_len = num_weights // num_prog
start_idx   = (section_len * prog_id_int)
end_idx = 0
if num_prog == (prog_id_int + 1):
    end_idx = num_weights - 1
else:
    end_idx = (section_len * prog_id_int) + section_len - 1
"""

# Create the thread class and give it a start and end index for the combination file.
class thread():
    start_idx = 0
    end_idx = 0
    num_games = 0
    def __init__(self, thread_name, thread_ID, start_idx, end_idx, num_games):
        # threading.Thread.__init__(self)
        self.thread_name = thread_name
        self.thread_ID = thread_ID
        self.start_idx = start_idx
        self.end_idx = end_idx
        self.num_games = num_games

    def run(self):

        # Number of weights we are looking to optimize
        num_weights = 9

        """
        Genetic algorithm parameters:
            Mating pool size
            Population size
        """
        solutions_per_pop  = 40
        num_parents_mating = 3

        # Defining the population size
        # The population will have sol_per_pop chromosome where each chromosome
        # has num_weights genes.
        pop_size = (solutions_per_pop, num_weights)
        # Create the initial population
        new_population = numpy.random.uniform(low=-1.0, high=1.0, size=pop_size)
        print(new_population)

        num_generations = 100
        for generation in range(num_generations):
            print("Generation: ", generation)
            # Measure the fitness of each chromosome in the population
            fitness = genetic_algorithm.cal_pop_fitness(new_population)
            # Best option
            for idx in range(len(new_population)):
                print("Weights: " + str(new_population[idx]))
                print("Fitness : ", fitness[idx])

                if (fitness[idx] > 0.55):
                    final_file_name = "results.txt"
                    final_file = open(final_file_name, "a")
                    final_file.write(str(new_population[idx]) + "\n" + str(fitness[idx]) + "\n")
                    final_file.close()

            # Selecting the best parents in the population for mating
            parents = genetic_algorithm.select_mating_pool(new_population, fitness, num_parents_mating)

            # Generating next generation using crossover
            offspring_crossover = genetic_algorithm.crossover(parents,
                                               offspring_size=(pop_size[0]-parents.shape[0], num_weights))

            # Adding some variations to the offspring using mutation
            offspring_mutation = genetic_algorithm.mutation(offspring_crossover)

            # Creating the new population based on the parents and offspring.
            new_population[0:parents.shape[0], :] = parents
            new_population[parents.shape[0]:, :] = offspring_mutation

        # Getting the best solution after iterating finishing all generations.
        #At first, the fitness is calculated for each solution in the final generation.
        fitness = genetic_algorithm.cal_pop_fitness(new_population)
        # Then return the index of that solution corresponding to the best fitness.
        best_match_idx = numpy.where(fitness == numpy.max(fitness))

        print("Best solution : ", new_population[best_match_idx, :])
        print("Best solution fitness : ", fitness[best_match_idx])

if __name__ == '__main__':

    # Initialize the thread and start it
    thread1 = thread("thread1", 1, 0, 0, 0)
    thread1.run()
