# game.py
# by Johnathon Beaumier
# for use in my program for playing the Guillotine card game

from random import shuffle
from copy import deepcopy
from guillotine.card import action_cards, noble_cards

DAYS = 3
STARTING_LINE_SIZE = 12
STARTING_ACTION_CARDS = 5


class Guillotine(object):

    def __init__(self, players):
        self.players = players
        self.line = []
        self.noble_deck = noble_cards
        self.action_deck = action_cards
        self.discard_pile = []

        self.current_player = None
        self.decision = None
        self.decider = None
        self.turn = 0

    def play(self):
        shuffle(self.players) # setup turn order
        self.deal_action_cards()

        # play the game

        for __ in range(DAYS):
            self.assemble_noble_line()

            while len(self.line) > 0:
                print(self.line)
                self.rotate_players()
                self.current_player.do_turn(self)

        # finish the game

        print('---')
        print('Scores')
        for player in self.players:
            print('{}: {} points'.format(player.name, player.score()))

    def rotate_players(self):
        self.players = self.players[1:] + [self.players[0]]
        self.current_player = self.players[0]

    def assemble_noble_line(self):
        shuffle(self.noble_deck)
        self.line = self.noble_deck[:STARTING_LINE_SIZE]
        self.noble_deck = self.noble_deck[STARTING_LINE_SIZE:]

    def deal_action_cards(self):
        shuffle(self.action_deck)
        for i, player in enumerate(self.players):
            start, end = i * STARTING_ACTION_CARDS, (i + 1) * STARTING_ACTION_CARDS 
            player.hand = self.action_deck[start:end]
        self.action_deck = self.action_deck[len(self.players)*STARTING_ACTION_CARDS:]
    
    def copy(self):
        return deepcopy(self)