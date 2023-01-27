from random import randint
import sys
from src.colour import Colour
from src.game import Game
from src.strategy_factory import StrategyFactory
from src.strategies import HumanStrategy

import src.weight

import os
import threading
import sys

import numpy
import ga

# Create the thread class and give it a start and end index for the combination file.
class thread():
    start_idx = 0
    end_idx = 0
    num_games = 0
    def __init__(self, thread_name, thread_ID):
        # threading.Thread.__init__(self)
        self.thread_name = thread_name
        self.thread_ID = thread_ID

    def run(self):
        # Number of weights we are looking to optimize
        num_weights = 8

        """
        Genetic algorithm parameters:
            Mating pool size
            Population size
        """
        solutions_per_pop  = 8
        num_parents_mating = 4

        # Defining the population size
        # The population will have sol_per_pop chromosome where each chromosome
        # has num_weights genes.
        pop_size = (solutions_per_pop, num_weights)
        # Create the initial population
        new_population = numpy.random.uniform(low=-1.0, high=1.0, size=pop_size)
        print(new_population)

        num_generations = 10000
        for generation in range(num_generations):
            print("Generation: ", generation)
            # Measure the fitness of each chromosome in the population
            fitness = ga.cal_pop_fitness(new_population)
            # Best option
            for idx in range(len(new_population)):
                print("Weights: " + str(new_population[idx]))
                print("Fitness : ", fitness[idx])

            # Selecting the best parents in the population for mating
            parents = ga.select_mating_pool(new_population, fitness, num_parents_mating)

            # Generating next generation using crossover
            offspring_crossover = ga.crossover(parents,
                                               offspring_size=(pop_size[0]-parents.shape[0], num_weights))

            # Adding some variations to the offspring using mutation
            offspring_mutation = ga.mutation(offspring_crossover)

            # Creating the new population based on the parents and offspring.
            new_population[0:parents.shape[0], :] = parents
            new_population[parents.shape[0]:, :] = offspring_mutation

        # Getting the best solution after iterating finishing all generations.
        #At first, the fitness is calculated for each solution in the final generation.
        fitness = ga.cal_pop_fitness(new_population)
        # Then return the index of that solution corresponding to the best fitness.
        best_match_idx = numpy.where(fitness == numpy.max(fitness))

        print("Best solution : ", new_population[best_match_idx, :])
        print("Best solution fitness : ", fitness[best_match_idx])

if __name__ == '__main__':

    # Initialize the thread and start it
    thread1 = thread("thread1", 1)
    thread1.run()
