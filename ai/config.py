from guillotine.card import action_cards
import random

DEFAULT_CONFIG = {'score': 10, 'actions': 1}
for card in action_cards:
    DEFAULT_CONFIG[card.name] = 1
DEFAULT_CONFIG['Filler Action'] = -1


def random_config():
    random_numbers = []
    for __ in range(2 + len(action_cards)):
        random_numbers.append(random.random())
    random_sum = sum(random_numbers)

    config = {}
    config['score'] = 10.0 * random_numbers[0] / random_sum
    config['actions'] = 10.0 * random_numbers[1] / random_sum
    for i, card in enumerate(action_cards):
        config[card.name] = (2.0 * random_numbers[i+2] - 1) / random_sum
    
    return config