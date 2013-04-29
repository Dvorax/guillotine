# player.py
# by Johnathon Beaumier
# for use in my program for playing the Guillotine card game

from guillotine import events
from ai.minmax import alpha_beta_search


class Player(object):

    def __init__(self, name):
        self.name = name
        self.hand = []
        self.score_pile = []

    def score(self):
        values = [card.value for card in self.score_pile]
        return sum(values)

    def make_decision(self, game, choices):
        # implemented in subclasses
        pass

    def __eq__(self, other):
        return self.name == other.name
    def __ne__(self, other):
        return self.name != other.name

    def __repr__(self):
        return self.name


class Human(Player):
    
    def make_decision(self, __, choices):
        for i, choice in enumerate(choices):
            print('{}: {}'.format(i+1, choice))

        # options start at index 1 for ease of typing on keyboard
        decision = raw_input('{}s Choice >> '.format(self.name))
        while decision not in [str(i+1) for i in range(len(choices))]:
            decision = raw_input('error >> ')

        # returns index of choice list
        return int(decision) - 1


class Computer(Player):

    def __init__(self, name, config=None):
        super(Computer, self).__init__(name)
        self.config = config

    def make_decision(self, game, choices):
        best_option, __ = alpha_beta_search(game, self)
        return best_option


class BadComputer(Computer):
    
    def make_decision(self, game, choices):
        return -1