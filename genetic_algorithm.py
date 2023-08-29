import numpy

from random import randint
import sys
from src.colour import Colour
from src.game import Game
from src.strategy_factory import StrategyFactory
from src.strategies import HumanStrategy

import src.weight

# This project is extended and a library called PyGAD is released to build the genetic algorithm.
# PyGAD documentation: https://pygad.readthedocs.io
# Install PyGAD: pip install pygad
# PyGAD source code at GitHub: https://github.com/ahmedfgad/GeneticAlgorithmPython

def cal_pop_fitness(pop):
    # Calculating the fitness value of each solution in the current population.
    # The fitness function caulcuates the sum of products between each input and its corresponding weight.
    fitness = []
    num_games = 500

    for row in pop:
        print(row)
        # Win count variables
        white_win_count = 0
        win_percentage_one  = 0.0
        # Run the desired number of games and check the win percentage
        for game_idx in range(0, num_games):
            # Initialize the game object
            game = Game(
                white_strategy=StrategyFactory.create_by_name("player2_achankins"),
                black_strategy=StrategyFactory.create_by_name("CompareAllMovesWeightingDistance"),
                first_player=Colour(randint(0, 1))
            )
            src.weight.init(row)
            # Run the backgammon game and output results to the output file
            game.run_game(verbose=False)
            if "white" == str(game.who_won()):
                white_win_count += 1
                print("White won: " + str(white_win_count / (game_idx + 1)))
            else:
                print("Black won: " + str(white_win_count / (game_idx + 1)))

            if (white_win_count / (game_idx + 1) <= 0.1 and game_idx == 100):
                break
            if (white_win_count / (game_idx + 1) <= 0.15 and game_idx == 200):
                break
            if (white_win_count / (game_idx + 1) <= 0.20 and game_idx == 300):
                break
            if (white_win_count / (game_idx + 1) <= 0.25 and game_idx == 300):
                break

        # Calculate the win percentage against the first strategy
        win_percentage_one = white_win_count / num_games
        # Take the average win percentage as our "fitness level"
        fitness.append(win_percentage_one)

    return fitness

def select_mating_pool(pop, fitness, num_parents):
    # Selecting the best individuals in the current generation as parents for producing the offspring of the next generation.
    parents = numpy.empty((num_parents, pop.shape[1]))
    for parent_num in range(num_parents):
        max_fitness_idx = numpy.where(fitness == numpy.max(fitness))
        max_fitness_idx = max_fitness_idx[0][0]
        parents[parent_num, :] = pop[max_fitness_idx, :]
        fitness[max_fitness_idx] = -99999999999
    return parents

def crossover(parents, offspring_size):
    offspring = numpy.empty(offspring_size)
    # The point at which crossover takes place between two parents. Usually it is at the center.
    crossover_point = numpy.uint8(offspring_size[1]/2)

    for k in range(offspring_size[0]):
        # Index of the first parent to mate.
        parent1_idx = k%parents.shape[0]
        # Index of the second parent to mate.
        parent2_idx = (k+1)%parents.shape[0]
        # The new offspring will have its first half of its genes taken from the first parent.
        offspring[k, 0:crossover_point] = parents[parent1_idx, 0:crossover_point]
        # The new offspring will have its second half of its genes taken from the second parent.
        offspring[k, crossover_point:] = parents[parent2_idx, crossover_point:]
    return offspring

def mutation(offspring_crossover):
    # Mutation changes a single gene in each offspring randomly.
    for idx in range(offspring_crossover.shape[0]):
        # The random value to be added to the gene.
        random_value = numpy.random.uniform(-1.0, 1.0, 1)
        offspring_crossover[idx, 4] = offspring_crossover[idx, 4] + random_value
    return offspring_crossover