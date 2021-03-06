# card.py
# by Johnathon Beaumier
# for use in my program for playing the Guillotine card game

from guillotine import events

# structure:
# method definition for helper function
# class definition for card types
# lists for card object creation and grouping


### Method Definitions #######################################################


# so far unused
def possible_other_hands(hand, size, discard):
    # make list of cards not accounted for
    # some are duplicates, so we cant use 'not in'
    possible_cards = list(action_cards)
    for card in hand + discard:
        possible_cards.remove(card)

    # return all combinations of *size* possible cards


### Class Definitions ########################################################


# TODO: Change card events to *events

class Card(object):

    def __init__(self, name, description, value, event_order):
        self.name = name
        self.description = description
        self.value = value
        if event_order is None:
            event_order = {} # in case events get activated, default parameters should not be mutable
        self.events = event_order

    def __repr__(self):
        if self.description is not None and self.value == 0:
            return '<{}> - {}'.format(self.name, self.description)
        elif self.description is not None:
            return '<{} ({})> - {}'.format(self.name, self.value, 
                    self.description)
        elif self.value == 0:
            return '<{}>'.format(self.name)
        else:
            return '<{} ({})>'.format(self.name, self.value)


class NobleCard(Card):

    categories = {'Church': 'blue', 'Military': 'red', 'Royal': 'purple', 
            'Negative': 'gray', 'Civic': 'green'}

    names = {}

    def __init__(self, name, value, category, description=None, 
            trigger='collection', event_order=None):
        super(NobleCard, self).__init__(name, description, value, event_order)
        self.category = category

        NobleCard.names[name] = value

    def color(self):
        return Noble.categories[self.category]


class ActionCard(Card):

    names = []
    
    def __init__(self, name, description, event_order, value=0):
        super(ActionCard, self).__init__(name, description, value, event_order)

        ActionCard.names.append(name)


### List Definitions #########################################################


# TODO: Card IDs to differentiate between same cards

noble_cards = [
        NobleCard('Mayor', 3, 'Civic'),
        NobleCard('Regent', 4, 'Royal'),
        NobleCard('Baron', 3, 'Royal'),
        NobleCard('Heretic', 2, 'Church'),
        NobleCard('Councilman', 3, 'Civic'),
        NobleCard('Bishop', 2, 'Church'),
        NobleCard('Piss Boy', 1, 'Royal'),
        NobleCard('Governor', 4, 'Civic'),
        NobleCard('Hero of the People', -3, 'Negative'),
        NobleCard('Tax Collector', 2, 'Civic'),
        NobleCard('Coiffeur', 1, 'Royal'),
        NobleCard('Duke', 3, 'Royal'),
        NobleCard('Colonel', 3, 'Military'),
        NobleCard('Archbishop', 4, 'Church'),
        NobleCard('King Louis XVI', 5, 'Royal'),
        NobleCard('Marie Antoinette', 5, 'Royal'),
        NobleCard('Bad Nun', 3, 'Church'),
        NobleCard('Royal Cartographer', 1, 'Royal'),
        NobleCard('Land Lord', 2, 'Civic')
] + 2 * [
        NobleCard('Wealthy Priest', 1, 'Church'),
        NobleCard('Sheriff', 1, 'Civic'),
        NobleCard('Lieutenant', 2, 'Military')
] + 3 * [
        NobleCard('Martyr', -1, 'Negative')
] + 20 * [
        NobleCard('Filler Noble', 0, 'Negative')
]

action_cards = 4 * [
        ActionCard('Fainting Spell', 
                'Move a noble backward up to 3 places in line.', [
                (events.choose_from_line, {'from_back': 1}),
                (events.choose_movement, {'distance': -3}),
                (events.move, {})
        ]), ActionCard('Was That My Name?', 
                'Move a noble forward up to 3 places in line.', [
                (events.choose_from_line, {'from_front': 1}),
                (events.choose_movement, {'distance': 3}),
                (events.move, {})
        ])
] + 8 * [
        ActionCard('Stumble', 
                'Move a noble forward exactly 1 place in line.', [
                (events.choose_from_line, {'from_front': 1}),
                (events.move, {'distance': 1})
        ]), ActionCard('Pushed', 
                'Move a noble forward exactly 2 places in line.', [
                (events.choose_from_line, {'from_front': 2}),
                (events.move, {'distance': 2})
        ]), ActionCard('Friend of the Queen', 
                'Move a noble backward up to 2 places in line.', [
                (events.choose_from_line, {'from_back': 1}),
                (events.choose_movement, {'distance': -2}),
                (events.move, {})
        ]), ActionCard('Ignoble Noble', 
                'Move a noble forward exactly 4 places in line.', [
                (events.choose_from_line, {'from_front': 4}),
                (events.move, {'distance': 4})
        ]), ActionCard("L'Idiot", 
                'Move a noble forward up to 2 places in line.', [
                (events.choose_from_line, {'from_front': 1}),
                (events.choose_movement, {'distance': 2}),
                (events.move, {})
        ])
] + 12 *[
        ActionCard('Filler Action', 
                'Placeholder card to fill the deck. No effect.', [])
]