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

def minimax_with_metrics(state, depth, maxPlayer):
    from ai.game_utils import is_terminal, utility
    nodes = 1
    
    if is_terminal(state) or depth == 0:
        if utility(state, 'X'):
            return 10, nodes
        elif utility(state, 'O'):
            return -10, nodes
        else:
            return 0, nodes
    
    possible_moves = actions(state)
    
    if maxPlayer:
        bestScore = float('-inf')
        for move in possible_moves:
            result(state, move, 'X')
            score, child_nodes = minimax_with_metrics(state, depth - 1, False)
            undo_move(state, move)
            nodes += child_nodes
            bestScore = max(bestScore, score)
    else:
        bestScore = float('inf')
        for move in possible_moves:
            result(state, move, 'O')
            score, child_nodes = minimax_with_metrics(state, depth - 1, True)
            undo_move(state, move)
            nodes += child_nodes
            bestScore = min(bestScore, score)
    
    return bestScore, nodes

def alphabeta_with_metrics(state, depth, maxPlayer, alpha, beta):
    from ai.game_utils import is_terminal, utility
    nodes = 1
    pruned = 0
    
    if is_terminal(state) or depth == 0:
        if utility(state, 'X'):
            return 10, nodes, pruned
        elif utility(state, 'O'):
            return -10, nodes, pruned
        else:
            return 0, nodes, pruned
    
    possible_moves = actions(state)
    
    if maxPlayer:
        bestScore = float('-inf')
        for i, move in enumerate(possible_moves):
            result(state, move, 'X')
            score, child_nodes, child_pruned = alphabeta_with_metrics(
                state, depth - 1, False, alpha, beta)
            undo_move(state, move)
            nodes += child_nodes
            pruned += child_pruned
            bestScore = max(bestScore, score)
            alpha = max(alpha, score)
            if beta <= alpha:
                pruned += len(possible_moves) - i - 1
                break
    else:
        bestScore = float('inf')
        for i, move in enumerate(possible_moves):
            result(state, move, 'O')
            score, child_nodes, child_pruned = alphabeta_with_metrics(
                state, depth - 1, True, alpha, beta)
            undo_move(state, move)
            nodes += child_nodes
            pruned += child_pruned
            bestScore = min(bestScore, score)
            beta = min(beta, score)
            if beta <= alpha:
                pruned += len(possible_moves) - i - 1
                break
    
    return bestScore, nodes, pruned

def get_best_move_with_metrics(state, depth, player, use_alphabeta=True):
    nodes_explored = 0
    nodes_pruned = 0
    
    best_move = None
    best_score = float('-inf') if player == 'X' else float('inf')
    
    possible_moves = actions(state)
    
    for move in possible_moves:
        result(state, move, player)
        
        if use_alphabeta:
            score, nodes, pruned = alphabeta_with_metrics(
                state, depth-1, player == 'O', 
                float('-inf'), float('inf'))
            nodes_explored += nodes
            nodes_pruned += pruned
        else:
            score, nodes = minimax_with_metrics(
                state, depth-1, player == 'O')
            nodes_explored += nodes
        
        undo_move(state, move)
        
        if (player == 'X' and score > best_score) or \
           (player == 'O' and score < best_score):
            best_score = score
            best_move = move
    
    return best_move, nodes_explored, nodes_pruned