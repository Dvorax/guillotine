# from guillotine.game import Guillotine
# from guillotine.player import Human, Computer, LazyComputer
# # from ai.config import random_config, DEFAULT_CONFIG
# from es.genome import Config
# from random import seed

# players = [
# 		# Comput('Ash'), 
# 		LazyComputer('Gary'), 
# 		Computer('Prof Oak', Config.random())
# ]

# seed()
# a = Guillotine(*players)
# a.play()

from __future__ import print_function
from es.algorithm import EvolutionStrategy
from es.genome import Config
import random

# Main module for my Evolution Strategy program
# Author: Johnathon Beaumier

if __name__ == "__main__":
    num_parents = 2
    num_offspring = 3
    default_step_size = 1.0
    termination_count = 100

    es = EvolutionStrategy(num_parents, num_offspring, default_step_size,
            termination_count)

    # print('Run # [-start-----------------------------------finish-]')

    for i in range(1):
        # print('---\nRun {0} '.format(i+1), end='')
        random.seed()
        population = [Config.random() for __ in range(num_parents)]
        solution = es.evolve(population)
        print('\n{0}: {1}'.format(solution, solution.evaluate()))
