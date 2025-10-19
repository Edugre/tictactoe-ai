from ai.state_utils import normalize
from ai.game_utils import utility, is_terminal, evaluate, actions, result, undo_move

def minimax(state, depth, maxPlayer, cache=None):
    nodes = 1

    if cache is None:
        cache = {}

    key = normalize(state)
    if key in cache:
        return cache[key], 0

    if is_terminal(state) or depth == 0:
        score = evaluate(state)
        cache[key] = score

        return score, nodes

    if maxPlayer:
        bestScore = float('-inf') 
        
        for move in actions(state):
            result(state, move, 'X')
            score, childNodes = minimax(state, depth - 1, False, cache)
            undo_move(state, move)
            nodes += childNodes
            bestScore = max(bestScore, score)
    
    else:
        bestScore = float('inf')

        for move in actions(state):
            result(state, move, 'O')
            score, childNodes = minimax(state, depth - 1, True, cache)
            undo_move(state, move)
            nodes += childNodes
            bestScore = min(bestScore, score)

    cache[key] = bestScore

    return bestScore, nodes
