# game.py
# by Johnathon Beaumier
# for use in my program for playing the Guillotine card game

from random import shuffle
# from copy import deepcopy
from guillotine.card import action_cards, noble_cards
from guillotine.events import STARTING_QUEUE
from guillotine.player import Computer, LazyComputer


class Guillotine(object):

    def __init__(self, *players):
        self.players = list(players)
        self.current_player = players[0]
        self.line = []
        self.noble_deck = list(noble_cards)
        self.action_deck = list(action_cards)
        self.discard_pile = []
        self.turn = 0
        self.day = 0

        self.event_queue = list(STARTING_QUEUE)
        self.decision = None
        self.stack = []
        self.print_statements = True
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
        if self.print_statements:
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

    def scores(self, perspective):
        descendant = self.descendant(perspective)
        others = list(set(self.players) - set([descendant]))
        other_scores = [player.score() for player in others]

        return descendant.score(), sum(other_scores)

    def descendant(self, perspective):
        index = self.players.index(perspective)
        return self.players[index]

    def is_game_over(self):
        return self.day > 3
    
    def copy(self):
        # deep copy was having issues with computation length
        players = [player.copy() for player in self.players]
        duplicate = Guillotine(*players)
        duplicate.current_player = self.current_player.copy()
        duplicate.line = list(self.line)
        duplicate.noble_deck = list(self.noble_deck)
        duplicate.action_deck = list(self.action_deck)
        duplicate.discard_pile = self.discard_pile
        duplicate.turn = self.turn
        duplicate.day = self.day

        duplicate.event_queue = list(self.event_queue)
        duplicate.decision = self.decision.copy()
        duplicate.stack = list(self.stack)
        duplicate.print_statements = self.print_statements
        duplicate.ai_deciding = self.ai_deciding
        duplicate.explore_random = self.explore_random

        return duplicate