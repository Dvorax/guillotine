import random
from guillotine import STARTING_ACTION_CARDS, STARTING_LINE_SIZE

# structure:
# class definitions for Decisions and some exceptions
# method definitions for events
# lists for default event queues


### Class Definitions ########################################################


class NoChoiceException(Exception):
    pass


class Decision(object):

    def __init__(self, decider, options):
        self.decider = decider
        self.options = options

        if len(self.options) == 0:
            raise NoChoiceException()

    def resolve(self, game, controlled_decision=None):
        if controlled_decision is None:
            decision_index = self.decider.make_decision(game, self.options)
        else:
            decision_index = controlled_decision

        game.stack.append(self.options[decision_index])
        game.decision = None


### Method Definitions #######################################################


def _string_reference(game, string):
    if string == 'current':
        return game.current_player
    elif string == 'current hand':
        return game.current_player.hand
    elif string == 'stack':
        return game.stack.pop()
    elif isinstance(string, str):
        raise Exception('unknown string reference')
    else:
        # string was not a str, pass it along
        return string

def choose_player(game, chooser='current'):
    print('choose player')

def choose_from_hand(game, chooser='current', hand_owner=None, 
        include_none=False):
    print('choose from hand')

    chooser = _string_reference(game, chooser)
    if hand_owner is None:
        hand_owner = chooser

    choices = hand_owner.hand if not include_none \
            else hand_owner.hand + ['No Action']
    
    game.decision = Decision(chooser, choices)

def choose_from_discard(game, chooser='current'):
    print('choose from discard')

def choose_from_line(game, chooser='current', category=None, 
        randomly_select=False, from_front=0, from_back=0):
    print('choose from line')
    if randomly_select:
        game.stack.append(random.choice(game.line))
        return

    chooser = _string_reference(game, chooser)

    start, end = from_front, len(game.line) - from_back
    choices = [noble for noble in game.line[start:end]
            if category is None or category == noble.category]

    game.decision = Decision(chooser, choices)

def choose_movement(game, chooser='current', distance=None):
    '''
    Presents the choice of movement distance to the player.
    Upto is implied over exact distances, else we would not give a choice
    Card to be moved has already been chosen, only resolves movement
    '''
    print('choose movement')
    chooser = _string_reference(game, chooser)

    if distance > 0:
        choices = range(1, distance + 1)
    else:
        choices = range(distance, 0)

    game.decision = Decision(chooser, choices)

def play_action(game):
    print('play action')

    card = game.stack[-1]
    if card != 'No Action':
        game.insert_events(*card.events)

def collect_noble(game, player='current'):
    print('collect noble')

    player = _string_reference(game, player)
    player.score_pile.append(game.line.pop(0))

def draw_action(game, player='current'):
    print('draw action')

    player = _string_reference(game, player)

    if len(game.action_deck) < 1:
        # ran out of cards in the action deck
        random.shuffle(game.discard_pile)
        game.action_deck = game.discard_pile
        game.discard_pile = []

    player.hand.append(game.action_deck.pop())

def move(game, distance='stack', position=None):
    # get origin from stack
    # if distance and position undefined, get distance from stack
    print('move')

    distance = _string_reference(game, distance)
    card = game.stack.pop()

    new_pos = game.line.index(card) - distance
    if new_pos < 0:
        new_pos = 0
    elif new_pos >= len(game.line):
        new_pos = len(game.line) - 1

    game.line.remove(card)
    game.line.insert(new_pos, card)

def rearrange_line(game, player='current', first_n=None):
    print('rearrange line')

def discard(game, location='current hand'):
    print('discard')

    card = game.stack.pop()
    if card != 'No Action':
        location = _string_reference(game, location)
        location.remove(card)
        game.discard_pile.append(card)

def assemble_noble_line(game):
    print('assemble noble line')

    random.shuffle(game.noble_deck)
    game.line = game.noble_deck[:STARTING_LINE_SIZE]
    game.noble_deck = game.noble_deck[STARTING_LINE_SIZE:]
    print(game.line)

def deal_action_cards(game):
    print('deal action cards')

    random.shuffle(game.action_deck)
    for i, player in enumerate(game.players):
        start, end = i * STARTING_ACTION_CARDS, (i + 1) * STARTING_ACTION_CARDS 
        player.hand = game.action_deck[start:end]
    game.action_deck = game.action_deck[len(game.players)*STARTING_ACTION_CARDS:]

def transition_turns(game):
    print('transition turns')

    # rotate players
    game.players = game.players[1:] + [game.players[0]]
    game.current_player = game.players[0]
    game.insert_events(
            (choose_from_hand, {'include_none': True}),
            (play_action, {}),
            (discard, {}),
            (collect_noble, {}),
            (draw_action, {}),
            (transition_turns, {})
    )

    # bookkeeping
    game.turn += 1
    if len(game.line) == 0:
        # do not automatically assemble noble line 
        # because the game may be over before it gets executed
        # and there is a (perhaps negligible) risk of running out of nobles
        game.insert_events((assemble_noble_line, {}))
        game.day += 1

    print(game.line)


### List Definitions #########################################################


STARTING_QUEUE = [
        (deal_action_cards, {}),
        (assemble_noble_line, {}),
        (choose_from_hand, {'include_none': True}),
        (play_action, {}),
        (discard, {}),
        (collect_noble, {}),
        (draw_action, {}),
        (transition_turns, {})
]