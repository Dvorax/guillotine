from random import uniform, gauss
from math import e, pi, sin, sqrt

# This module implements the specific problem for our assignemnt
# Author: Johnathon Beaumier

class X(object):
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
        self.variables = variables
        self.step_sizes = step_sizes

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

        x1, x2 = self.variables
        return 21.5 + x1 * sin(4*pi*x1) + x2 * sin(20*pi*x2)

    def is_viable(self):
        '''
        Determines if this instance is a viable solution
        out: boolean corresponding to the solution's viablitiy
        '''
        if len(self) != 2 or len(self.step_sizes) != 2:
            raise Exception('Incorrect form for Variables or Step Sizes')

        x1, x2 = self.variables
        return -3.0 <= x1 <= 12.0 and 4.0 <= x2 <= 6.0

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
        for i in range(len(self)):
            mutation.step_sizes[i] *= step_size_modifier(len(self))
            mutation.variables[i] += self.step_sizes[i] * gauss(0, 1)

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

        child_vars = []
        for parent_vars in zip(self.variables, other_parent.variables):
            child_vars.append(1.0 * sum(parent_vars) / len(parent_vars))

        return X(child_vars, self.step_sizes)

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
        x1, x2 = self.variables

        if x1 < -3:
            self.variables[0] = -3.0
        elif x1 > 12:
            self.variables[0] = 12.0

        if x2 < 4:
            self.variables[1] = 4.0
        elif x2 > 6:
            self.variables[1] = 6.0

    def __len__(self):
        return len(self.variables)

    def __getitem__(self, key):
        # keys start at 1 so they match the variable naming pattern
        return self.variables[key-1]

    def __repr__(self):
        vector_str = str(self.variables).replace('[','{').replace(']','}')
        return 'X = ' + vector_str

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
        variables = [uniform(-3.0, 12.0), uniform(4.0, 6.0)]
        step_sizes = [1.0, 1.0]

        return X(variables, step_sizes)
