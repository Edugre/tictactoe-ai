import pytest
from ai.minimax import minimax, utility, is_terminal, evaluate, actions, result, undo_move, is_draw

def test_empty_board():
    """Test minimax on empty board"""
    state = [[None, None, None], [None, None, None], [None, None, None]]
    score = minimax(state, 9, True)
    assert score == 0  # Perfect play should result in draw

def test_winning_move_x():
    """Test X can win in one move"""
    state = [['X', 'X', None], ['O', 'O', None], [None, None, None]]
    score = minimax(state, 3, True)
    assert score == 10  # X should win

def test_blocking_move():
    """Test algorithm blocks opponent's winning move"""
    state = [['O', 'O', None], ['X', None, None], [None, None, None]]
    score = minimax(state, 5, True)
    # X should block O's win, resulting in eventual draw or win for X
    assert score >= 0

def test_terminal_states():
    """Test evaluation of terminal states"""
    # X wins
    x_win = [['X', 'X', 'X'], ['O', 'O', None], [None, None, None]]
    assert utility(x_win, 'X') == True
    assert evaluate(x_win) == 10
    
    # O wins  
    o_win = [['O', 'O', 'O'], ['X', 'X', None], [None, None, None]]
    assert utility(o_win, 'O') == True
    assert evaluate(o_win) == -10
    
    # Draw
    draw = [['X', 'O', 'X'], ['O', 'X', 'O'], ['O', 'X', 'O']]
    assert is_draw(draw) == True
    assert evaluate(draw) == 0

def test_actions_generation():
    """Test available moves are correctly identified"""
    state = [['X', None, 'O'], [None, 'X', None], ['O', None, None]]
    moves = actions(state)
    expected = [(0,1), (1,0), (1,2), (2,1), (2,2)]
    assert sorted(moves) == sorted(expected)

def test_result_and_undo():
    """Test making and undoing moves"""
    state = [[None, None, None], [None, None, None], [None, None, None]]
    
    # Make move
    result(state, (1,1), 'X')
    assert state[1][1] == 'X'
    
    # Undo move
    undo_move(state, (1,1))
    assert state[1][1] is None

def test_diagonal_wins():
    """Test diagonal win detection"""
    # Main diagonal
    diag1 = [['X', 'O', 'O'], ['O', 'X', 'O'], ['O', 'O', 'X']]
    assert utility(diag1, 'X') == True
    
    # Anti-diagonal
    diag2 = [['O', 'O', 'X'], ['O', 'X', 'O'], ['X', 'O', 'O']]
    assert utility(diag2, 'X') == True

def test_depth_limiting():
    """Test minimax with depth limit"""
    state = [[None, None, None], [None, None, None], [None, None, None]]
    
    # Shallow depth should still return reasonable score
    score = minimax(state, 2, True)
    assert isinstance(score, (int, float))

if __name__ == "__main__":
    pytest.main([__file__])