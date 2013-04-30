import random
# from es.genome import Config
# from ai.config import DEFAULT_CONFIG
from guillotine.card import action_cards, NobleCard


def utility(game_state, perspective):
    
    # if isinstance(perspective.config, str) and perspective.config == 'Bad': 
    #     config = {'Was That My Name?': -0.721736658666746, 
    #             'Filler Action': 0.35161674398506104, 
    #             'Pushed': 0.7012137370924143, 
    #             'actions': 8.396797605350429, 
    #             'Ignoble Noble': -0.32337105481579465, 
    #             'score': 2.954374972277405, 
    #             'Friend of the Queen': -0.698393339565728, 
    #             'Fainting Spell': -0.41902459339210885, 
    #             "L'Idiot": -0.0771939380719644, 
    #             'Stumble': -0.42298449036881847}
    # el
    if perspective.config is not None:
        config = perspective.config
    else:
        # default config
        config = NobleCard.names
        # config = {'score': 10.0, 'actions': 1.0}
        # for card in action_cards:
        #     config[card.name] = 1.0
        # config['Filler Action'] = -1.0

    # config = perspective.config
    # for card in action_cards:
    #     config.variables[card.name] = 1.0
    # config.variables['Filler Action'] = -0.5

    # descendant_score, other_scores = game_state.scores(perspective)
    # utility = config['score'] * (descendant_score - other_scores)

    descendant = game_state.descendant(perspective)

    # utility = noble_scores = 0
    utility = 0
    for card in descendant.score_pile:
        utility += config[card.name]
        # noble_scores += config[card.name]
    # utility += config['nobles'] * noble_scores

    # action_scores = 0
    # for card in descendant.hand:
    #     if card.name == 'Filler Action':
    #         action_scores += -0.5
    #     else:
    #         action_scores += 1.0
    # utility += action_scores

    # weight of cards in each % len(players) slot


    return utility

    # return 0
    
def result(game_state, decision):
    game_copy = game_state.copy()
    game_copy.ai_deciding = True
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

        # if alpha >= beta:
        #     break

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
# =
        # if alpha >= beta:
        #     break

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

    if game_state.print_statements:
        print("Best value from utility: {0}".format(best_value))
    return best_option, best_value