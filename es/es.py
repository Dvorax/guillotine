from __future__ import print_function
import random
import sys

# This module is the engine for my Evolution Strategy algorithm
# Author: Johnathon Beaumier

class EvolutionStrategy(object):
    # '''
    # Class that implements the Evolution Strategy algorithm
    # '''

    def __init__(self, num_parents, num_offspring, default_step_size, 
            termination_count):
        '''
        Constructor for the Evolution Strategy class
        which sets a few parameters
        in:  integer for the number of parents
             integer for the number of offspring
             float for the default_step_size
             integer for the termination_count
        '''
        self.num_parents = num_parents
        self.num_offspring = num_offspring
        self.default_step_size = default_step_size
        self.termination_count = termination_count

    def evolve(self, population, show_progress=True):
        '''
        Primary algorithm of the EvolutionStrategy class
        in:  list for the population being evolved
             (optional) boolean for showing progress as periods on the screen
        out: the best of run individual
        '''
        best_individual = random.choice(population)

        for generation in range(self.termination_count):
            children = self.make_children(population)
            population = self.select_survivors(children)
            
            if max(population) > best_individual:
                best_individual = max(population)

            if show_progress and generation % 200 == 0:
                print('.', end='')
                sys.stdout.flush()

        return best_individual

    def make_children(self, parents):
        '''
        Produces children from a set of parents
        in:  list of parents
        out: list of children
        '''
        # for each offspring, choose 2 random parents and 
        # recombine them to make an offspring then mutate it 
        children = []

        for __ in range(self.num_offspring):
            parent_a = random.choice(parents)
            parent_b = random.choice(parents)
            child = parent_a.recombine(parent_b)
            children.append(child.mutate())

        return children

    def select_survivors(self, children):
        '''
        Selects survivors for the next generation
        in:  list of children
        out: list of survivors, the parents of the next generation
        '''
        # (mu, lambda) selection
        # deterministic survivor selection from only offspring
        return sorted(children)[-self.num_parents:]
