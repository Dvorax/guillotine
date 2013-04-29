# game.py
# by Johnathon Beaumier
# for use in my program for playing the Guillotine card game

from random import shuffle
from copy import deepcopy
from guillotine.card import action_cards, noble_cards
from guillotine.events import STARTING_QUEUE


class Guillotine(object):

    def __init__(self, players):
        self.players = players
        self.current_player = players[0]
        self.line = []
        self.noble_deck = noble_cards
        self.action_deck = action_cards
        self.discard_pile = []
        self.turn = 0
        self.day = 0

        self.event_queue = STARTING_QUEUE
        self.decision = None
        self.stack = []
        # self.print_statements = True
        self.ai_deciding = False
        self.explore_random = False

    def play(self):
        # randomize starting turn order
        shuffle(self.players) 

        # play the game
        while not self.is_game_over():
            self.advance()
            self.decision.resolve(self)

        # finish the game
        print('---')
        print('Scores')
        for player in self.players:
            print('{}: {} points'.format(player.name, player.score()))

    def advance(self):
        while self.decision is None:
            event, parameters = self.event_queue.pop(0)
            event(self, **parameters)

    def insert_events(self, *events):
        for event in reversed(events):
            self.event_queue.insert(0, event)

    def is_game_over(self):
        return self.day > 3
    
    def copy(self):
        return deepcopy(self)