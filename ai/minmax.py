import random

def alpha_beta_search(game_state, depth):
    weights = game_state.current_player.config

    if game_state.current_player.side == 'north':
        best_pit, best_value = Algorithm._min_value(game_state, depth, float("-inf"), float("inf"), weights)
    else:
        best_pit, best_value = Algorithm._max_value(game_state, depth, float("-inf"), float("inf"), weights)

    print("Best value from utility: {0}".format(best_value))
    return best_pit, best_value

def _max_value(game_state, depth, alpha, beta, weights):

    if Algorithm.terminal_test(game_state, depth):
        return -1, Algorithm.utility(game_state, weights)
    
    if game_state.current_player.side == 'north':
        possible_moves = game_state.possible_moves('north')
    else:
        possible_moves = game_state.possible_moves('south')

    best_pit = -1
    for pit in possible_moves:
        __, value = Algorithm._min_value(Algorithm.result(game_state, pit), depth - 1, alpha, beta, weights)

        # alpha = max(alpha, value)
        if value > alpha:
            alpha = value
            best_pit = pit

        if alpha >= beta:
            break

    return best_pit, alpha

def _min_value(game_state, depth, alpha, beta, weights):
    if Algorithm.terminal_test(game_state, depth):
        return -1, Algorithm.utility(game_state, weights)

    if game_state.current_player.side == 'north':
        possible_moves = game_state.possible_moves('south')
    else:
        possible_moves = game_state.possible_moves('north')

    best_pit = -1
    for pit in possible_moves:
        __, value = Algorithm._max_value(Algorithm.result(game_state, pit), depth - 1, alpha, beta, weights)

        if value < beta:
            beta = value
            best_pit = pit

        if alpha >= beta:
            break

    return best_pit, beta

def terminal_test(game_state, depth):
    if depth == 0:
        return True
    else:
        return game_state.is_game_over()

# Written from the perspective of south. Higher values indicate a good state for south.
# Negative values can be returned, indicating the state to be in favor of north.
def utility(game_state, weights):
    return 0

def result(game_state, pit_index):
    game_copy = game_state.copy()
    game_copy.move_stones(pit_index)
    return game_copy