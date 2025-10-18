def minimax(state, depth, maxPlayer):
    if is_terminal(state) or depth == 0:
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

def utility(state, player):
    for row in range(3):
        if state[row][0] == player and state[row][1] == player and state[row][2] == player:
            return True
        
    for col in range(3):
        if state[0][col] == player and state[1][col] == player and state[2][col] == player:
            return True
        
    if state[0][0] == player and state[1][1] == player and state[2][2] == player:
        return True
    
    if state[0][2] == player and state[1][1] == player and state[2][0] == player:
        return True
    
    return False

def is_terminal(state):
    return utility(state, 'X') or utility(state, 'O') or is_draw(state)    

def evaluate(state):
    if utility(state, 'X'):
        return 10
    elif utility(state, 'O'):
        return -10
    else:
        return 0

def actions(state): 
    moves = []
    for row in range(3):
        for col in range(3):
            if state[row][col] is None:
                moves.append((row, col))
    
    return moves

def result(state, move, sign): 
    row, col = move

    state[row][col] = sign

def undo_move(state, move): 
    row, col = move

    state[row][col] = None

def is_draw(state):
    for row in range(3):
        for col in range(3):
            if state[row][col] is None:
                return False
            
    return True