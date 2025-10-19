# 🕹️ Tic-Tac-Toe AI

## Introduction
This project implements an AI player for Tic-Tac-Toe using **Minimax** and **Alpha-Beta Pruning**. The code also includes **state symmetry normalization** (hashing equivalent boards) to avoid re-computing identical positions under rotation/flip. We compare correctness and efficiency between plain Minimax and Alpha-Beta. 

To run the program:
`python main.py`
Using Python 3.x.

## Task 
Tic-Tac-Toe is a two-player game on a 3×3 board.
- Players X and O take turns marking empty cells.
- The first player to align three symbols in a row wins.
- If the board fills with no winner, the game ends in a draw.

### Board Representation:
- X → Player 1
- O → Player 2
- _ → Empty cell
 
## Algorithms

### Minimax

The Minimax algorithm simulates all possible moves, alternating between maximizing and minimizing turns. It anticipates the opponent’s responses and selects the optimal sequence of moves.

### Alpha-Beta Pruning

Alpha-Beta Pruning optimizes Minimax by pruning branches that cannot affect the final outcome. Both algorithms use caching and state normalization to avoid recomputing equivalent board states.

## Symmetry Hashing

The `normalize()` function generates all rotations and reflections of the board and selects the canonical tuple representation. This ensures symmetric states are evaluated only once, improving efficiency.

## Game Rules & Evaluation
-	`utility()` – checks all rows, columns, and diagonals for a win.
-	`is_terminal()` – detects if the game has reached a win or draw.
-	`evaluate()` – returns:
    -	+10 if X wins
    -	−10 if O wins
    -	0 if it’s a draw
-	`actions()` – lists available empty cells.
-	`result()` / undo_move() – simulate and revert moves during AI decision-making.

## Performance, Discussion & Future Work

The Tic-Tac-Toe branching factor reaches up to nine moves at the start, leading to exponential growth in the Minimax search tree. Alpha-Beta Pruning produces the same optimal results but explores fewer nodes, reducing computation time.

Caching and symmetry reduction further improve efficiency without affecting correctness.

### Minimax Plays First
| Algorithm   | Move number | Decision time (ms) | Nodes explored | Pruned nodes | Pruning efficiency |
|------------|-------------|------------------|----------------|--------------|------------------|
| Minimax    | 1           | 294              | 5467           | N/A          | N/A              |
| Alpha-Beta | 2           | 53               | 1259           | 1036         | 45.10%           |
| Minimax    | 3           | 44               | 869            | N/A          | N/A              |
| Alpha-Beta | 4           | 9                | 144            | 106          | 42.40%           |
| Minimax    | 5           | 9                | 129            | N/A          | N/A              |
| Alpha-Beta | 6           | 3                | 30             | 8            | 21.10%           |
| Minimax    | 7           | 1                | 13             | N/A          | N/A              |
| Alpha-Beta | 8           | 0                | 4              | 0            | 0.00%            |
| Minimax    | 9           | 0                | 1              | N/A          | N/A              |

### Alpha-Beta Plays First
| Algorithm   | Move number | Decision time (ms) | Nodes explored | Pruned nodes | Pruning efficiency |
|------------|-------------|------------------|----------------|--------------|------------------|
| Alpha-Beta | 1           | 130              | 3401           | 2854         | 45.60%           |
| Minimax    | 2           | 86               | 1736           | N/A          | N/A              |
| Alpha-Beta | 3           | 27               | 511            | 398          | 43.80%           |
| Minimax    | 4           | 21               | 338            | N/A          | N/A              |
| Alpha-Beta | 5           | 7                | 111            | 29           | 20.70%           |
| Minimax    | 6           | 4                | 37             | N/A          | N/A              |
| Alpha-Beta | 7           | 2                | 13             | 0            | 0.00%            |
| Minimax    | 8           | 1                | 4              | N/A          | N/A              |
| Alpha-Beta | 9           | 0                | 1              | 0            | 0.00%            |

Both Minimax and Alpha-Beta guarantee **optimal play**, but Alpha-Beta achieves it with **significantly reduced computation time**.

## Additional Features

### Export Game to CSV 
After each game, moves, board states, nodes explored, decision times, and pruning statistics can be exported to a CSV file. This allows algorithm performance comparison across multiple games.

## Implementation Details
- Language: Python 3.x
- Libraries: Tkinter (GUI), CSV, and standard Python libraries

Key Functions:
get_best_move, actions, result, undo_move, utility, is_terminal, evaluate, normalize, minimax, alphabeta.

## Conclusion
This project demonstrates an AI for Tic-Tac-Toe using Minimax and Alpha-Beta Pruning with state symmetry optimization. It highlights the efficiency gains of Alpha-Beta over plain Minimax and provides tools to analyze algorithm performance through CSV export. Future enhancements could include heuristic evaluation for mid-game states, move ordering, or extending the AI to larger boards like Connect-Four.
