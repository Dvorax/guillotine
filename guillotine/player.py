# player.py
# by Johnathon Beaumier
# for use in my program for playing the Guillotine card game

from guillotine import events
# from guillotine.ai.minmax import alpha_beta_search


class Player(object):

    def __init__(self, name):
        self.name = name
        self.hand = []
        self.score_pile = []

    def score(self):
        score = 0
        for card in self.score_pile:
            score += card.value

        return score

    def do_turn(self, game):
        stack = []

        try:
            events.choose_from_hand(game, stack, include_none=True)
            events.play_action(game, stack)
            events.discard(game, stack)
        except events.NothingPlayedException:
            pass

        events.collect_noble(game, stack)

        events.draw_action(game, stack)

    def make_decision(self, game, choices):
        # implement this in subclasses
        pass


class Human(Player):
    
    def make_decision(self, __, choices):
        for i, choice in enumerate(choices):
            print('{}: {}'.format(i+1, choice))

        decision = raw_input('Your Choice >> ')
        while decision not in [str(i+1) for i in range(len(choices))]:
            decision = raw_input('error >> ')

        # returns index of choice list
        return int(decision) - 1


class Computer(Player):
    
    def make_decision(self, game, choices):
        return 0