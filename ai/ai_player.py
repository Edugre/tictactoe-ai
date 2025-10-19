from ai.game_utils import actions, result, undo_move
from ai.minimax import minimax
from ai.alphabeta import alphabeta

def get_best_move(state, depth, player, use_alphabeta=True):
    nodes_explored = 0
    nodes_pruned = 0
    
    best_move = None
    best_score = float('-inf') if player == 'X' else float('inf')
    
    possible_moves = actions(state)
    
    for move in possible_moves:
        result(state, move, player)
        
        if use_alphabeta:
            score, nodes, pruned = alphabeta(
                state, depth-1, player == 'O', 
                float('-inf'), float('inf'))
            nodes_explored += nodes
            nodes_pruned += pruned
        else:
            score, nodes = minimax(
                state, depth-1, player == 'O')
            nodes_explored += nodes
        
        undo_move(state, move)
        
        if (player == 'X' and score > best_score) or \
           (player == 'O' and score < best_score):
            best_score = score
            best_move = move
    
    return best_move, nodes_explored, nodes_pruned