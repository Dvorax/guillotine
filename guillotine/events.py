import random

class NoUseException(Exception):
    pass


class NothingPlayedException(Exception):
    pass


def _string_reference(game, stack, string):
    if string == 'current':
        return game.current_player
    elif string == 'current hand':
        return game.current_player.hand
    elif string == 'stack':
        return stack.pop()
    elif isinstance(string, str):
        raise Exception('unknown string reference')
    else:
        # string was not a str, pass it along
        return string

def _ask_choice(game, chooser, choices):
    if len(choices) > 1:
        choice_index = chooser.make_decision(game, choices)
        return choices[choice_index]
    elif len(choices) > 0:
        return choices[0]
    else:
        raise NoUseException()


def choose_player(game, stack, chooser='current'):
    print('choose player')

def choose_from_hand(game, stack, chooser='current', hand_owner=None, include_none=False):
    print('choose from hand')

    chooser = _string_reference(game, stack, chooser)
    if hand_owner is None:
        hand_owner = chooser

    choices = hand_owner.hand if not include_none \
            else hand_owner.hand + ['No Action']
    stack.append(_ask_choice(game, chooser, choices))

    if stack[-1] == 'No Action':
        raise NothingPlayedException()

def choose_from_discard(game, stack, chooser='current'):
    print('choose from discard')

def choose_from_line(game, stack, chooser='current', category=None, randomly_select=False, from_front=0, from_back=0):
    print('choose from line')
    if randomly_select:
        stack.append(random.choice(game.line))
        return

    chooser = _string_reference(game, stack, chooser)

    start, end = from_front, len(game.line) - from_back
    choices = [noble for noble in game.line[start:end]
            if category is None or category == noble.category]

    stack.append(_ask_choice(game, chooser, choices))

def choose_movement(game, stack, chooser='current', distance=None):
    '''
    Presents the choice of movement distance to the player.
    Upto is implied over exact distances, else we would not give a choice
    Card to be moved has already been chosen, only resolves movement
    '''
    print('choose movement')
    chooser = _string_reference(game, stack, chooser)

    if distance > 0:
        choices = range(1, distance + 1)
    else:
        choices = range(distance, 0)

    stack.append(_ask_choice(game, chooser, choices))

def play_action(game, stack):
    print('play action')
    card = stack[-1]
    card.use(game)

def collect_noble(game, stack, player='current'):
    print('collect noble')
    player = _string_reference(game, stack, player)
    player.score_pile.append(game.line.pop(0))

def draw_action(game, stack, player='current'):
    print('draw action')
    player = _string_reference(game, stack, player)

    if len(game.action_deck) < 1:
        random.shuffle(game.discard_pile)
        game.action_deck = game.discard_pile
        game.discard_pile = []

    player.hand.append(game.action_deck.pop())

def move(game, stack, distance='stack', position=None):
    # get origin from stack
    # if distance and position undefined, get distance from stack
    print('move')
    distance = _string_reference(game, stack, distance)
    card = stack.pop()

    new_pos = game.line.index(card) - distance
    if new_pos < 0:
        new_pos = 0
    elif new_pos >= len(game.line):
        new_pos = len(game.line) - 1

    game.line.remove(card)
    game.line.insert(new_pos, card)

def rearrange_line(game, stack, player='current', first_n=None):
    print('rearrange line')

def discard(game, stack, location='current hand'):
    print('discard')
    card = stack.pop()
    location = _string_reference(game, stack, location)
    location.remove(card)
    game.discard_pile.append(card)

