from ai.game_utils import actions, result, undo_move
from ai.minimax import minimax
from ai.alphabeta import alphabeta

def get_best_move(state, depth, player, use_alphabeta=True):
    best_move = None
    best_score = float('-inf') if player == 'X' else float('inf')

    for move in actions(state):
        result(state, move, player)

        if use_alphabeta:
            score = alphabeta(state, depth-1, player=='O', float('-inf'), float('inf'))
        else:
            score = minimax(state, depth-1, player=='O')

        undo_move(state, move)

        if (player == 'X' and score > best_score) or (player == 'O' and score < best_score):
            best_score = score
            best_move = move

    return best_move