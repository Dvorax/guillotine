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

    def __init__(self, decider, options, random_outcome=False):
        self.decider = decider
        self.options = list(options)
        self.random_outcome = random_outcome

        if len(self.options) == 0:
            raise NoChoiceException()

    def resolve(self, game, controlled_decision=None):
        if len(self.options) == 1:
            decision_index = 0
        elif controlled_decision is None:
            decision_index = self.decider.make_decision(game, self.options)
        else:
            decision_index = controlled_decision

        game.stack.append(self.options[decision_index])
        game.decision = None

        if game.print_statements and not game.ai_deciding:
            print('  {} --> {}'.format(self.decider, game.stack[-1]))

    def copy(self):
        return Decision(self.decider.copy(), self.options, self.random_outcome)


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
    if game.print_statements and not game.ai_deciding:
        print('choose player')

def choose_from_hand(game, chooser='current', hand_owner=None, 
        include_none=False):
    if game.print_statements and not game.ai_deciding:
        print('choose from hand')

    chooser = _string_reference(game, chooser)
    if hand_owner is None:
        hand_owner = chooser

    choices = hand_owner.hand if not include_none \
            else hand_owner.hand + ['No Action']
    
    game.decision = Decision(chooser, choices)

def choose_from_discard(game, chooser='current'):
    if game.print_statements and not game.ai_deciding:
        print('choose from discard')

def choose_from_line(game, chooser='current', category=None, 
        randomly_select=False, from_front=0, from_back=0):
    if game.print_statements and not game.ai_deciding:
        print('choose from line')

    if randomly_select:
        game.stack.append(random.choice(game.line))
        return

    chooser = _string_reference(game, chooser)

    start, end = from_front, len(game.line) - from_back
    choices = [noble for noble in game.line[start:end]
            if category is None or category == noble.category]

    if len(choices) == 0:
        choices = ['No Options']

    game.decision = Decision(chooser, choices)

def choose_movement(game, chooser='current', distance=None):
    '''
    Presents the choice of movement distance to the player.
    Upto is implied over exact distances, else we would not give a choice
    Card to be moved has already been chosen, only resolves movement
    '''
    if game.print_statements and not game.ai_deciding:
        print('choose movement')

    chooser = _string_reference(game, chooser)
    card = game.stack[-1]

    if card == 'No Options':
        choices = ['No Options']
    elif distance > 0:
        # if game.line.index(card) - distance < 0:
        #     pass
        #     # distance = game.line.index(card)
        choices = range(1, distance + 1)
    else:
        # if game.line.index(card) - distance >= len(game.line):
        #     pass
        #     # distance = game.line.index(card) - len(game.line)
        choices = range(-1, distance - 1, -1)

    try:
        game.decision = Decision(chooser, choices)
    except:
        print('card {}, distance {}'.format(game.line.index(card), distance))
        quit()

def play_action(game):
    if game.print_statements and not game.ai_deciding:
        print('play action')

    card = game.stack[-1]
    if card != 'No Action':
        game.insert_events(*card.events)

def collect_noble(game, player='current'):
    if game.print_statements and not game.ai_deciding:
        print('collect noble')

    player = _string_reference(game, player)
    player.score_pile.append(game.line.pop(0))

def draw_action(game, player='current'):
    if game.print_statements and not game.ai_deciding:
        print('draw action')

    player = _string_reference(game, player)

    if len(game.action_deck) < 1:
        # ran out of cards in the action deck
        random.shuffle(game.discard_pile)
        game.action_deck = game.discard_pile
        game.discard_pile = []

    if not game.explore_random:
        player.hand.append(game.action_deck.pop())
    else:
        game.decision = Decision(player, game.action_deck, random_outcome=True)
        def stack_to_hand(game):
            player = _string_reference(game, 'current')
            player.hand.append(game.stack.pop())
        game.insert_events((stack_to_hand, {}))

def move(game, distance='stack', position=None):
    # get origin from stack
    # if distance and position undefined, get distance from stack
    if game.print_statements and not game.ai_deciding:
        print('move')

    distance = _string_reference(game, distance)
    card = game.stack.pop()

    if 'No Options' not in [card, distance]:
        new_pos = game.line.index(card) - distance

        game.line.remove(card)
        game.line.insert(new_pos, card)

def rearrange_line(game, player='current', first_n=None):
    if game.print_statements and not game.ai_deciding:
        print('rearrange line')

def discard(game, location='current hand'):
    if game.print_statements and not game.ai_deciding:
        print('discard')

    card = game.stack.pop()
    if card != 'No Action':
        if game.print_statements and not game.ai_deciding:
            print('Removed {}'.format(card))
        location = _string_reference(game, location)
        location.remove(card)
        game.discard_pile.append(card)

def assemble_noble_line(game):
    if game.print_statements and not game.ai_deciding:
        print('assemble noble line')

    random.shuffle(game.noble_deck)
    game.line = game.noble_deck[:STARTING_LINE_SIZE]
    game.noble_deck = game.noble_deck[STARTING_LINE_SIZE:]

    if game.print_statements and not game.ai_deciding:
        print(game.line)

def deal_action_cards(game):
    if game.print_statements and not game.ai_deciding:
        print('deal action cards')

    random.shuffle(game.action_deck)
    for i, player in enumerate(game.players):
        start, end = i * STARTING_ACTION_CARDS, (i + 1) * STARTING_ACTION_CARDS 
        player.hand = game.action_deck[start:end]
    game.action_deck = game.action_deck[len(game.players)*STARTING_ACTION_CARDS:]

def transition_turns(game):
    if game.print_statements and not game.ai_deciding:
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

    if game.print_statements and not game.ai_deciding:
        print(game.turn)
        print(game.line)
        print(game.current_player.hand)


### List Definitions #########################################################


STARTING_QUEUE = [
        (deal_action_cards, {}),
        (transition_turns, {})
]
