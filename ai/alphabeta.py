from ai.state_utils import normalize
from ai.game_utils import utility, is_terminal, evaluate, actions, result, undo_move

def alphabeta(state, depth, maxPlayer, alpha, beta, cache=None):
    nodes = 1
    pruned = 0

    if cache is None:
        cache = {}

    key = normalize(state)
    if key in cache:
        return cache[key], 0, 0

    if is_terminal(state) or depth == 0:
        score = evaluate(state)
        cache[key] = score

        return score, nodes, pruned

    if maxPlayer:
        bestScore = float('-inf') 

        possibleMoves = actions(state)
        for i, move in enumerate(possibleMoves):
            result(state, move, 'X')
            score, childNodes, prunedNodes = alphabeta(state, depth - 1, False, alpha, beta, cache)
            undo_move(state, move)
            nodes += childNodes
            pruned += prunedNodes
            bestScore = max(bestScore, score)
            alpha = max(alpha, score)

            if beta <= alpha:
                pruned += len(possibleMoves) - i - 1
                break
    
    else:
        bestScore = float('inf')

        possibleMoves = actions(state)
        for i, move in enumerate(possibleMoves):
            result(state, move, 'O')
            score, childNodes, prunedNodes = alphabeta(state, depth - 1, True, alpha, beta, cache)
            undo_move(state, move)
            nodes += childNodes
            pruned += prunedNodes
            bestScore = min(bestScore, score)
            beta = min(beta, score)

            if beta <= alpha:
                pruned += len(possibleMoves) - i - 1
                break

    cache[key] = bestScore
    return bestScore, nodes, pruned