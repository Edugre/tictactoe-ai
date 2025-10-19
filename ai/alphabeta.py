from ai.state_utils import normalize
from ai.minimax import utility, is_terminal, evaluate, actions, result, undo_move, is_draw

def alphabeta(state, depth, maxPlayer, alpha, beta, cache=None):
    if cache is None:
        cache = {}

    key = normalize(state)
    if key in cache:
        return cache[key]

    if is_terminal(state) or depth == 0:
        score = evaluate(state)
        cache[key] = score

        return score

    if maxPlayer:
        bestScore = float('-inf') 
        
        for move in actions(state):
            result(state, move, 'X')
            score = alphabeta(state, depth - 1, False, alpha, beta, cache)
            undo_move(state, move)
            bestScore = max(bestScore, score)
            alpha = max(alpha, score)

            if beta <= alpha:
                break
    
    else:
        bestScore = float('inf')

        for move in actions(state):
            result(state, move, 'O')
            score = alphabeta(state, depth - 1, True, alpha, beta, cache)
            undo_move(state, move)
            bestScore = min(bestScore, score)
            beta = min(beta, score)

            if beta <= alpha:
                break

    cache[key] = bestScore
    return bestScore