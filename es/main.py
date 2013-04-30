from __future__ import print_function
from es.algorithm import EvolutionStrategy
from es.genome import Config
import random

# Main module for my Evolution Strategy program
# Author: Johnathon Beaumier

if __name__ == "__main__":
    num_parents = 3
    num_offspring = 21
    default_step_size = 1.0
    termination_count = 100

    es = EvolutionStrategy(num_parents, num_offspring, default_step_size,
            termination_count)

    print('Run # [-start-----------------------------------finish-]')

    for i in range(10):
        print('---\nRun {0} '.format(i+1), end='')
        random.seed()
        population = [Config.random() for __ in range(num_parents)]
        solution = es.evolve(population)
        print('\n{0}: {1}'.format(solution, solution.evaluate()))
        # 11.139937353408085, 5.125049495845527}: 37.5692830554
