from random import uniform, gauss, seed
from math import e, pi, sin, sqrt
from guillotine.card import NobleCard, ActionCard
from guillotine.player import Computer, LazyComputer
from guillotine.game import Guillotine

# This module implements the specific problem for our assignemnt
# Author: Johnathon Beaumier

class Config(object):
# '''
# Class for solving the problem of maximizing the function f through evolution
# f(x1, x2) = 21.5 + x1 * sin(4*pi*x1) + x2 * sin(20*pi*x2)
# '''

    def __init__(self, variables, step_sizes):
        '''
        Initializes a new instance if class X
        in:  list of floats of length 2 for variables
             list of floats of length 2 for step sizes
        '''
        self.variables = dict(variables)
        self.step_sizes = dict(step_sizes)

        if not self.is_viable():
            self.enforce_bounds()

    def evaluate(self):
        '''
        Evaluates the quality of this instance
        out: float representing the quality of this instance
        '''
        if not self.is_viable():
            raise Exception('Error - Trying to Evaluate ' + \
                    'Unviable Individual: {0}'.format(self))

        self_scores = other_scores = 0

        # for i in range(10):
        #     # seed(i) 
        #     game = Guillotine(
        #             Computer('Config Bot', self), 
        #             LazyComputer('Lazy Bot'))
        #     game.print_statements = False
        #     game.play()

        #     self_score, other_score = game.scores(Computer('Config Bot', self))
        #     self_scores += self_score
        #     other_scores += other_score

        for i in range(20):
            # seed(i)
            game = Guillotine(
                    Computer('Config Bot', self), 
                    Computer('Decent Bot'))
            game.print_statements = False
            game.play()

            descendant = game.descendant(Computer('Config Bot', self))
            for card in descendant.score_pile:
                self_scores += card.value ** 7
            # self_score, other_score = game.scores(Computer('Config Bot', self))
            # self_scores += self_score
            # other_scores += other_score

        # seed()

        return self_scores / 10000.0
        # return self_scores / 10.0 + other_scores / 10000.0#- other_scores

    def square_difference(self):
        difference = 0

        for key, value in NobleCard.names.items():
            difference += (self.variables[key] - value) ** 2

        return difference

    def is_viable(self):
        '''
        Determines if this instance is a viable solution
        out: boolean corresponding to the solution's viablitiy
        '''

        for key, variable in self.variables.items():
            special_keys = ['nobles', 'actions']

            if key in special_keys and (variable < 0 or variable > 100):
                return False
            elif key in NobleCard.names and (variable < -3 or variable > 5):
                return False
            elif  key in ActionCard.names and (variable < -1 or variable > 1):
                return False

        return True

    def mutate(self):
        '''
        Produces a mutated form of the current instance
        out: X instance of a mutation
        '''

        def step_size_modifier(n):
            tau_prime = 1 / sqrt(2 * n)
            tau = 1 / sqrt(2 * sqrt(n))
            return e**(tau_prime * gauss(0, 1) + tau * gauss(0, 1))

        mutation = self.clone()
        for key in self.variables:
            mutation.step_sizes[key] *= step_size_modifier(len(self))
            mutation.variables[key] += self.step_sizes[key] * gauss(0, 1)

        if not mutation.is_viable():
            mutation.enforce_bounds()

        return mutation

    def recombine(self, other_parent):
        '''
        Does recombination with another parent to produce an offspring
        out: X instance of an offspring
        '''
        # using intermediary recombination - average of both parents
        # other options: discrete recombination - choose one

        child_vars = {}
        for key in self.variables:
            parent_vars = self.variables[key], other_parent.variables[key]
            child_vars[key] = sum(parent_vars) / 2.0

        return Config(child_vars, self.step_sizes)

    def clone(self):
        '''
        Clones the current instance to a new one
        out: X instance of a clone
        '''
        return self.__class__(self.variables, self.step_sizes)

    def enforce_bounds(self):
        '''
        Enforces the bounds of the problem, 
        snapping variables back to the closest edge
        '''
        for key in self.variables:
            
            if key in NobleCard.names:
                if self.variables[key] <-3:
                    self.variables[key] = -3
                elif self.variables[key] > 5:
                    self.variables[key] = 5
            elif key in ActionCard.names:
                if self.variables[key] < -1:
                    self.variables[key] = -1
                elif self.variables[key] > 1:
                    self.variables[key] = 1
            else:
                if self.variables[key] < 0:
                    self.variables[key] = 0
                elif self.variables[key] > 100:
                    self.variables[key] = 100

    def __len__(self):
        return len(self.variables)

    def __getitem__(self, key):
        return self.variables[key]

    def __repr__(self):
        vector_str = str(self.variables).replace('[','{').replace(']','}')
        return 'Config = ' + vector_str

    # comparison operatations
    def __lt__(self, other):
        return self.evaluate() < other.evaluate()
    def __gt__(self, other):
        return self.evaluate() > other.evaluate()
    def __eq__(self, other):
        return self.evaluate() == other.evaluate()
    def __le__(self, other):
        return self.evaluate() <= other.evaluate()
    def __ge__(self, other):
        return self.evaluate() >= other.evaluate()
    def __ne__(self, other):
        return self.evaluate() != other.evaluate()

    @staticmethod
    def random():
        '''
        Produces an instance of X with random variable values
        out: X instance with random values
        '''
        # variables = [uniform(-3.0, 12.0), uniform(4.0, 6.0)]
        # step_sizes = [1.0, 1.0]

        # return X(variables, step_sizes)

        variables, step_sizes = {}, {}
        # for special_key in ['nobles', 'actions']:
        #     variables[special_key] = uniform(0.0, 100.0)
        #     step_sizes[special_key] = 1.0
        for card_name in NobleCard.names:
            variables[card_name] = uniform(-3.0, 5.0)
            step_sizes[card_name] = 1.0
        # for card_name in ActionCard.names:
        #     variables[card_name] = uniform(-1.0, 1.0)
        #     step_sizes[card_name] = 0.25
        
        return Config(variables, step_sizes)
