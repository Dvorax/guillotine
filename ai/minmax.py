import random
from ai.config import DEFAULT_CONFIG

def utility(game_state, perspective):
    descendant_index = game_state.players.index(perspective)
    descendant = game_state.players[descendant_index]
    others = list(set(game_state.players) - set([descendant]))
    other_scores = [player.score() for player in others]

    # config = {'score': 5, 'Stumble': 1, 'Pushed': 1, 
    #         'Friend of the Queen': 1, 'Ignoble Noble': 1, "L'Idiot": 1, 
    #         'Fainting Spell': 1, 'Was That My Name?': 1, 'Filler Action': -0.1}

    if descendant.config is None:
        config = DEFAULT_CONFIG
    else:
        config = descendant.config

    utility = config['score'] * (descendant.score() - sum(other_scores))

    action_config = 0
    for card in descendant.hand:
        action_config += config[card.name]
    utility += config['actions'] * action_config

    # weight of cards in each % len(players) slot
    # value of cards in hand



    return utility
    

def result(game_state, decision):
    game_copy = game_state.copy()
    game_copy.ai_deciding = True
    # game_copy.print_statements = False
    # game_copy.explore_random = True
    game_copy.decision.resolve(game_copy, decision)
    game_copy.advance()
    return game_copy

def terminal_test(game_state, depth):
    if depth == game_state.turn:
        return True
    else:
        return game_state.is_game_over()

def _max_value(game_state, perspective, depth, alpha, beta):

    if terminal_test(game_state, depth):
        return -1, utility(game_state, perspective)

    best_option = -1
    for option in range(len(game_state.decision.options)):
        __, value = _appropriate_value(result(game_state, option), 
                perspective, depth, alpha, beta)

        if value > alpha:
            alpha = value
            best_option = option

        if alpha >= beta:
            break

    return best_option, alpha

def _min_value(game_state, perspective, depth, alpha, beta):
    if terminal_test(game_state, depth):
        return -1, utility(game_state, perspective)

    best_option = -1
    for option in range(len(game_state.decision.options)):
        __, value = _appropriate_value(result(game_state, option), 
                perspective, depth, alpha, beta)

        if value < beta:
            beta = value
            best_option = option

        if alpha >= beta:
            break

    return best_option, beta

def _avg_value(game_state, perspective, depth, alpha, beta):
    if terminal_test(game_state, depth):
        return -1, utility(game_state, perspective)

    branch_values = []
    for option in range(len(game_state.decision.options)):
        __, value = _appropriate_value(result(game_state, option), 
                perspective, depth, alpha, beta)

        branch_values.append(value)

    average = 1.0 * sum(branch_values) / len(branch_values)

    return None, average

def _appropriate_value(game_state, perspective, depth, alpha, beta):
    if game_state.decision.random_outcome:
        return _avg_value(game_state, perspective, depth, alpha, beta)
    elif perspective == game_state.decision.decider:
        return _max_value(game_state, perspective, depth, alpha, beta)
    else:
        return _min_value(game_state, perspective, depth, alpha, beta)

def alpha_beta_search(game_state, perspective, depth=1):
    depth += game_state.turn

    best_option, best_value = _appropriate_value(game_state, perspective, 
            depth, float("-inf"), float("inf"))

    print("Best value from utility: {0}".format(best_value))
    return best_option, best_value