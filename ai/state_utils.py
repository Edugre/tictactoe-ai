def normalize(state):
    transformations = []
    
    current = state
    for _ in range(4):
        transformations.append(current)
        transformations.append(flip_horizontal(current))
        current = rotate_90(current)
    
    return min(transformations, key=state_to_tuple)


def state_to_tuple(s):
    return tuple(tuple(row) for row in s)

def rotate_90(state):
    new_state = [['_', '_', '_'], ['_', '_', '_'], ['_', '_', '_']]
    
    for row in range(3):
        for col in range(3):
            new_state[col][2 - row] = state[row][col]

    return new_state

def flip_horizontal(state):
    new_state = [['_', '_', '_'], ['_', '_', '_'], ['_', '_', '_']]
    
    for row in range(3):
        for col in range(3):
            new_state[row][2 - col] = state[row][col]
    
    return new_state

def flip_vertical(state):
    new_state = [['_', '_', '_'], ['_', '_', '_'], ['_', '_', '_']]
    
    for row in range(3):
        for col in range(3):
            new_state[2 - row][col] = state[row][col]
    
    return new_state
