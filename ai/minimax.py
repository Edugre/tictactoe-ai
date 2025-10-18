def minimax(state, depth, maxPlayer):
    if depth == 0 or is_terminal(state):
        return evaluate(state)
    
    if maxPlayer:
        bestScore = float('-inf') 
        
        for move in actions(state):
            result(state, move, 'X')
            score = minimax(state, depth - 1, False)
            undo_move(state, move)
            bestScore = max(bestScore, score)
        
        return bestScore
    
    else:
        bestScore = float('inf')

        for move in actions(state):
            result(state, move, 'O')
            score = minimax(state, depth - 1, True)
            undo_move(state, move)
            bestScore = min(bestScore, score)

        return bestScore

def is_terminal(state): #TODO
    return    

def evaluate(state): #TODO
    return    

def actions(state): #TODO
    return

def result(state, move, sign): #TODO
    return

def undo_move(state, move): #TODO
    return
