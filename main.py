import tkinter as tk
from tkinter import messagebox
import time
from ai.game_utils import utility, is_terminal
from ai.ai_player import get_best_move

class TicTacToeUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe with AI")
        self.root.geometry("800x700")
        self.root.resizable(False, False)
        
        self.reset_game_state()
        self.show_mode_selection()
    
    def reset_game_state(self):
        self.board = [['_', '_', '_'], ['_', '_', '_'], ['_', '_', '_']]
        self.current_player = 'X'
        self.game_mode = None
        self.human_is_x = True
        self.ai1_algorithm = None
        self.ai2_algorithm = None
        self.game_active = False
        self.nodes_explored = 0
        self.nodes_pruned = 0
        self.decision_time = 0
        self.buttons = []
    
    def show_mode_selection(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        title = tk.Label(self.root, text="Tic-Tac-Toe with AI", 
                        font=("Arial", 28, "bold"), fg="#2c3e50")
        title.pack(pady=40)
        
        subtitle = tk.Label(self.root, text="Select Game Mode", 
                           font=("Arial", 16), fg="#7f8c8d")
        subtitle.pack(pady=10)
        
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=30)
        
        modes = [
            ("Human vs Human", "HvH"),
            ("Human vs AI", "HvAI"),
            ("AI vs AI", "AIvAI")
        ]
        
        for text, mode in modes:
            btn = tk.Button(button_frame, text=text, font=("Arial", 14),
                           width=20, height=2, bg="#3498db", fg="white",
                           activebackground="#2980b9", cursor="hand2",
                           command=lambda m=mode: self.select_mode(m))
            btn.pack(pady=10)
    
    def select_mode(self, mode):
        self.game_mode = mode
        if mode == "HvH":
            self.show_first_player_selection()
        elif mode == "HvAI":
            self.show_human_ai_config()
        else:
            self.show_ai_vs_ai_config()
    
    def show_first_player_selection(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        title = tk.Label(self.root, text="Who Plays First?", 
                        font=("Arial", 24, "bold"), fg="#2c3e50")
        title.pack(pady=50)
        
        first_var = tk.StringVar(value="X")
        
        tk.Radiobutton(self.root, text="Player 1 (X)", variable=first_var, 
                       value="X", font=("Arial", 14)).pack(pady=10)
        tk.Radiobutton(self.root, text="Player 2 (O)", variable=first_var, 
                       value="O", font=("Arial", 14)).pack(pady=10)
        
        start_btn = tk.Button(self.root, text="Start Game", font=("Arial", 14, "bold"),
                             bg="#27ae60", fg="white", width=15, height=2,
                             command=lambda: self.start_hvh_game(first_var.get()))
        start_btn.pack(pady=30)
        
        tk.Button(self.root, text="Back", font=("Arial", 10),
                 command=self.show_mode_selection).pack()
    
    def show_human_ai_config(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        title = tk.Label(self.root, text="Human vs AI Configuration", 
                        font=("Arial", 24, "bold"), fg="#2c3e50")
        title.pack(pady=30)
        
        first_label = tk.Label(self.root, text="Who plays first?", 
                              font=("Arial", 14), fg="#34495e")
        first_label.pack(pady=10)
        
        first_var = tk.StringVar(value="Human")
        tk.Radiobutton(self.root, text="Human", variable=first_var, 
                      value="Human", font=("Arial", 12)).pack()
        tk.Radiobutton(self.root, text="AI", variable=first_var, 
                      value="AI", font=("Arial", 12)).pack()
        
        algo_label = tk.Label(self.root, text="Select AI Algorithm", 
                             font=("Arial", 14), fg="#34495e")
        algo_label.pack(pady=20)
        
        algo_var = tk.StringVar(value="alphabeta")
        tk.Radiobutton(self.root, text="Alpha-Beta Pruning", variable=algo_var, 
                      value="alphabeta", font=("Arial", 12)).pack()
        tk.Radiobutton(self.root, text="Minimax", variable=algo_var, 
                      value="minimax", font=("Arial", 12)).pack()
        
        start_btn = tk.Button(self.root, text="Start Game", font=("Arial", 14, "bold"),
                             bg="#27ae60", fg="white", width=15, height=2,
                             command=lambda: self.start_hvai_game(first_var.get(), algo_var.get()))
        start_btn.pack(pady=30)
        
        tk.Button(self.root, text="Back", font=("Arial", 10),
                 command=self.show_mode_selection).pack()
    
    def show_ai_vs_ai_config(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        title = tk.Label(self.root, text="AI vs AI Configuration", 
                        font=("Arial", 24, "bold"), fg="#2c3e50")
        title.pack(pady=30)
        
        ai1_frame = tk.LabelFrame(self.root, text="AI 1 (X)", font=("Arial", 12, "bold"),
                                 padx=20, pady=15)
        ai1_frame.pack(pady=10, padx=50, fill="x")
        
        ai1_var = tk.StringVar(value="alphabeta")
        tk.Radiobutton(ai1_frame, text="Alpha-Beta Pruning", variable=ai1_var, 
                      value="alphabeta", font=("Arial", 11)).pack(anchor="w")
        tk.Radiobutton(ai1_frame, text="Minimax", variable=ai1_var, 
                      value="minimax", font=("Arial", 11)).pack(anchor="w")
        
        ai2_frame = tk.LabelFrame(self.root, text="AI 2 (O)", font=("Arial", 12, "bold"),
                                 padx=20, pady=15)
        ai2_frame.pack(pady=10, padx=50, fill="x")
        
        ai2_var = tk.StringVar(value="alphabeta")
        tk.Radiobutton(ai2_frame, text="Alpha-Beta Pruning", variable=ai2_var, 
                      value="alphabeta", font=("Arial", 11)).pack(anchor="w")
        tk.Radiobutton(ai2_frame, text="Minimax", variable=ai2_var, 
                      value="minimax", font=("Arial", 11)).pack(anchor="w")
        
        start_label = tk.Label(self.root, text="Who starts?", 
                              font=("Arial", 14), fg="#34495e")
        start_label.pack(pady=10)
        
        first_var = tk.StringVar(value="X")
        tk.Radiobutton(self.root, text="AI 1 (X)", variable=first_var, 
                      value="X", font=("Arial", 12)).pack()
        tk.Radiobutton(self.root, text="AI 2 (O)", variable=first_var, 
                      value="O", font=("Arial", 12)).pack()
        
        start_btn = tk.Button(self.root, text="Start Game", font=("Arial", 14, "bold"),
                             bg="#27ae60", fg="white", width=15, height=2,
                             command=lambda: self.start_aivai_game(ai1_var.get(), 
                                                                   ai2_var.get(), 
                                                                   first_var.get()))
        start_btn.pack(pady=20)
        
        tk.Button(self.root, text="Back", font=("Arial", 10),
                 command=self.show_mode_selection).pack()
    
    def start_hvh_game(self, first_player):
        self.current_player = first_player
        self.show_game_board()
    
    def start_hvai_game(self, first_player, algorithm):
        self.ai1_algorithm = algorithm
        self.human_is_x = (first_player == "Human")
        self.current_player = 'X'
        self.show_game_board()
        
        if first_player == "AI":
            self.root.after(500, self.ai_make_move)
    
    def start_aivai_game(self, ai1_algo, ai2_algo, first):
        self.ai1_algorithm = ai1_algo
        self.ai2_algorithm = ai2_algo
        self.current_player = first
        self.show_game_board()
        self.root.after(500, self.ai_vs_ai_step)
    
    def show_game_board(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.game_active = True
        
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        top_frame = tk.Frame(main_frame)
        top_frame.pack(fill="x", pady=(0, 15))
        
        title = tk.Label(top_frame, text="Tic-Tac-Toe", 
                        font=("Arial", 20, "bold"), fg="#2c3e50")
        title.pack(side="left")
        
        self.turn_label = tk.Label(top_frame, text=f"Turn: {self.get_player_name()}", 
                                   font=("Arial", 16, "bold"), fg="#e74c3c")
        self.turn_label.pack(side="right")
        
        content_frame = tk.Frame(main_frame)
        content_frame.pack(fill="both", expand=True)
        
        board_frame = tk.Frame(content_frame)
        board_frame.pack(side="left", padx=(0, 20))
        
        self.buttons = []
        for row in range(3):
            button_row = []
            for col in range(3):
                btn = tk.Button(board_frame, text="", font=("Arial", 40, "bold"),
                              width=4, height=2, bg="#ecf0f1",
                              command=lambda r=row, c=col: self.make_move(r, c))
                btn.grid(row=row, column=col, padx=2, pady=2)
                button_row.append(btn)
            self.buttons.append(button_row)
        
        metrics_frame = tk.LabelFrame(content_frame, text="Performance Metrics", 
                                     font=("Arial", 14, "bold"), padx=15, pady=15)
        metrics_frame.pack(side="right", fill="both", expand=True)
        
        algo_name = self.get_current_algorithm_name()
        if algo_name:
            algo_label = tk.Label(metrics_frame, text=algo_name, 
                                 font=("Arial", 12, "bold"), 
                                 fg="#3498db" if "Alpha-Beta" in algo_name else "#9b59b6")
            algo_label.pack(pady=(0, 10))
        
        tk.Label(metrics_frame, text="Decision Time:", 
                font=("Arial", 11), fg="#34495e").pack(anchor="w")
        self.time_label = tk.Label(metrics_frame, text="0ms", 
                                   font=("Arial", 11, "bold"), fg="#27ae60")
        self.time_label.pack(anchor="w", pady=(0, 10))
        
        tk.Label(metrics_frame, text="Nodes Explored:", 
                font=("Arial", 11), fg="#34495e").pack(anchor="w")
        self.nodes_label = tk.Label(metrics_frame, text="0", 
                                    font=("Arial", 11, "bold"), fg="#2980b9")
        self.nodes_label.pack(anchor="w", pady=(0, 10))
        
        tk.Label(metrics_frame, text="Pruning Efficiency:", 
                font=("Arial", 11), fg="#34495e").pack(anchor="w")
        self.pruning_label = tk.Label(metrics_frame, text="N/A", 
                                      font=("Arial", 11, "bold"), fg="#e67e22")
        self.pruning_label.pack(anchor="w")
        
        button_frame = tk.Frame(main_frame)
        button_frame.pack(pady=15)
        
        tk.Button(button_frame, text="Restart Game", font=("Arial", 11),
                 bg="#f39c12", fg="white", width=12,
                 command=self.restart_game).pack(side="left", padx=5)
        
        tk.Button(button_frame, text="Change Mode", font=("Arial", 11),
                 bg="#95a5a6", fg="white", width=12,
                 command=self.change_mode).pack(side="left", padx=5)
    
    def get_player_name(self):
        if self.game_mode == "HvH":
            return f"Player {'1' if self.current_player == 'X' else '2'} ({self.current_player})"
        elif self.game_mode == "HvAI":
            if self.is_ai_turn():
                return f"AI ({self.current_player})"
            else:
                return f"Human ({self.current_player})"
        else:
            return f"AI {'1' if self.current_player == 'X' else '2'} ({self.current_player})"
    
    def get_current_algorithm_name(self):
        if self.game_mode == "HvH":
            return None
        elif self.game_mode == "HvAI":
            algo = self.ai1_algorithm
        else:
            algo = self.ai1_algorithm if self.current_player == 'X' else self.ai2_algorithm
        
        return "Alpha-Beta Pruning" if algo == "alphabeta" else "Minimax Algorithm"
    
    def is_ai_turn(self):
        if self.game_mode == "HvH":
            return False
        elif self.game_mode == "HvAI":
            return (self.current_player == 'X' and not self.human_is_x) or \
                   (self.current_player == 'O' and self.human_is_x)
        else:
            return True
    
    def make_move(self, row, col):
        if not self.game_active or self.board[row][col] != '_':
            return
        
        if self.is_ai_turn():
            return
        
        self.board[row][col] = self.current_player
        self.update_button(row, col)
        
        if self.check_game_over():
            return
        
        self.current_player = 'O' if self.current_player == 'X' else 'X'
        self.turn_label.config(text=f"Turn: {self.get_player_name()}")
        
        if self.game_mode == "HvAI" and self.is_ai_turn():
            self.root.after(500, self.ai_make_move)
    
    def ai_make_move(self):
        if not self.game_active:
            return
        
        start_time = time.time()
        
        if self.game_mode == "AIvAI":
            use_alphabeta = (self.current_player == 'X' and self.ai1_algorithm == "alphabeta") or \
                          (self.current_player == 'O' and self.ai2_algorithm == "alphabeta")
        else:
            use_alphabeta = self.ai1_algorithm == "alphabeta"
        
        best_move, self.nodes_explored, self.nodes_pruned = get_best_move(
            self.board, 9, self.current_player, use_alphabeta)
        
        end_time = time.time()
        self.decision_time = (end_time - start_time) * 1000
        
        if best_move:
            row, col = best_move
            self.board[row][col] = self.current_player
            self.update_button(row, col)
            self.update_metrics()
            
            if self.check_game_over():
                return
            
            self.current_player = 'O' if self.current_player == 'X' else 'X'
            self.turn_label.config(text=f"Turn: {self.get_player_name()}")
        
    def update_metrics(self):
        self.time_label.config(text=f"{self.decision_time:.0f}ms")
        self.nodes_label.config(text=f"{self.nodes_explored}")
        
        algo = None
        if self.game_mode == "HvAI":
            algo = self.ai1_algorithm
        else:
            algo = self.ai2_algorithm if self.current_player == 'O' else self.ai1_algorithm
        
        if algo == "alphabeta" and (self.nodes_explored + self.nodes_pruned) > 0:
            efficiency = (self.nodes_pruned / (self.nodes_explored + self.nodes_pruned)) * 100
            self.pruning_label.config(text=f"{efficiency:.1f}%")
        else:
            self.pruning_label.config(text="N/A")
    
    def ai_vs_ai_step(self):
        if not self.game_active:
            return
        
        self.ai_make_move()
        
        if self.game_active and not is_terminal(self.board):
            self.root.after(1000, self.ai_vs_ai_step)
    
    def update_button(self, row, col):
        symbol = self.board[row][col]
        color = "#e74c3c" if symbol == 'X' else "#3498db"
        self.buttons[row][col].config(text=symbol, fg=color, 
                                      disabledforeground=color, state="disabled")
    
    def check_game_over(self):
        if utility(self.board, 'X'):
            self.game_active = False
            winner = self.get_winner_name('X')
            messagebox.showinfo("Game Over", f"{winner} wins!")
            return True
        elif utility(self.board, 'O'):
            self.game_active = False
            winner = self.get_winner_name('O')
            messagebox.showinfo("Game Over", f"{winner} wins!")
            return True
        elif is_terminal(self.board):
            self.game_active = False
            messagebox.showinfo("Game Over", "It's a draw!")
            return True
        return False
    
    def get_winner_name(self, symbol):
        if self.game_mode == "HvH":
            return f"Player {'1' if symbol == 'X' else '2'}"
        elif self.game_mode == "HvAI":
            if (symbol == 'X' and not self.human_is_x) or (symbol == 'O' and self.human_is_x):
                return "AI"
            else:
                return "Human"
        else:
            return f"AI {'1' if symbol == 'X' else '2'}"
    
    def restart_game(self):
        current_mode = self.game_mode
        current_human_is_x = self.human_is_x
        current_ai1 = self.ai1_algorithm
        current_ai2 = self.ai2_algorithm
        
        self.reset_game_state()
        
        self.game_mode = current_mode
        self.human_is_x = current_human_is_x
        self.ai1_algorithm = current_ai1
        self.ai2_algorithm = current_ai2
        
        self.show_game_board()
        
        if self.game_mode == "HvAI" and not self.human_is_x:
            self.root.after(500, self.ai_make_move)
        elif self.game_mode == "AIvAI":
            self.root.after(500, self.ai_vs_ai_step)
    
    def change_mode(self):
        self.reset_game_state()
        self.show_mode_selection()

if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToeUI(root)
    root.mainloop()