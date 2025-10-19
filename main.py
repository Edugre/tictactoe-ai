import tkinter as tk
from tkinter import messagebox, filedialog
import time
import csv
from datetime import datetime
from ai.game_utils import utility, is_terminal
from ai.ai_player import get_best_move

class TicTacToeUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe with AI")
        self.root.geometry("800x700")
        self.root.resizable(False, False)
        self.root.configure(bg="#f8f9fa")  # Light gray background
        
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
        self.game_data = []
        self.game_start_time = None
        self.move_number = 0
    
    def show_mode_selection(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Main container frame to center content
        main_frame = tk.Frame(self.root, bg="#f8f9fa")
        main_frame.pack(expand=True, fill="both")
        
        # Center frame for content
        center_frame = tk.Frame(main_frame, bg="#f8f9fa")
        center_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        title = tk.Label(center_frame, text="Tic-Tac-Toe with AI", 
                        font=("Arial", 28, "bold"), fg="#2c3e50", bg="#f8f9fa")
        title.pack(pady=(0, 20))
        
        subtitle = tk.Label(center_frame, text="Select Game Mode", 
                           font=("Arial", 16), fg="#7f8c8d", bg="#f8f9fa")
        subtitle.pack(pady=(0, 30))
        
        button_frame = tk.Frame(center_frame, bg="#f8f9fa")
        button_frame.pack()
        
        modes = [
            ("Human vs Human", "HvH"),
            ("Human vs AI", "HvAI"),
            ("AI vs AI", "AIvAI")
        ]
        
        for text, mode in modes:
            btn = tk.Label(button_frame, text=text, font=("Arial", 14),
                          width=20, height=2, bg="#3498db", fg="white",
                          cursor="hand2", relief="raised", borderwidth=2)
            btn.bind("<Button-1>", lambda e, m=mode: self.select_mode(m))
            btn.bind("<Enter>", lambda e: e.widget.config(bg="#2980b9"))
            btn.bind("<Leave>", lambda e: e.widget.config(bg="#3498db"))
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
        
        # Main container frame to center content
        main_frame = tk.Frame(self.root, bg="#f8f9fa")
        main_frame.pack(expand=True, fill="both")
        
        # Center frame for content
        center_frame = tk.Frame(main_frame, bg="#f8f9fa")
        center_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        title = tk.Label(center_frame, text="Who Plays First?", 
                        font=("Arial", 24, "bold"), fg="#2c3e50", bg="#f8f9fa")
        title.pack(pady=(0, 30))
        
        first_var = tk.StringVar(value="X")
        
        tk.Radiobutton(center_frame, text="Player 1 (X)", variable=first_var, 
                       value="X", font=("Arial", 14), bg="#f8f9fa", fg="#2c3e50").pack(pady=10)
        tk.Radiobutton(center_frame, text="Player 2 (O)", variable=first_var, 
                       value="O", font=("Arial", 14), bg="#f8f9fa", fg="#2c3e50").pack(pady=10)
        
        start_btn = tk.Label(center_frame, text="Start Game", font=("Arial", 14, "bold"),
                            bg="#27ae60", fg="white", width=15, height=2,
                            cursor="hand2", relief="raised", borderwidth=2)
        start_btn.bind("<Button-1>", lambda e: self.start_hvh_game(first_var.get()))
        start_btn.bind("<Enter>", lambda e: e.widget.config(bg="#229954"))
        start_btn.bind("<Leave>", lambda e: e.widget.config(bg="#27ae60"))
        start_btn.pack(pady=30)
        
        back_btn = tk.Label(center_frame, text="Back", font=("Arial", 12),
                            bg="#6c757d", fg="white", width=10, height=1,
                            cursor="hand2", relief="raised", borderwidth=2)
        back_btn.bind("<Button-1>", lambda e: self.show_mode_selection())
        back_btn.bind("<Enter>", lambda e: e.widget.config(bg="#5a6268"))
        back_btn.bind("<Leave>", lambda e: e.widget.config(bg="#6c757d"))
        back_btn.pack()
    
    def show_human_ai_config(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Main container frame to center content
        main_frame = tk.Frame(self.root, bg="#f8f9fa")
        main_frame.pack(expand=True, fill="both")
        
        # Center frame for content
        center_frame = tk.Frame(main_frame, bg="#f8f9fa")
        center_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        title = tk.Label(center_frame, text="Human vs AI Configuration", 
                        font=("Arial", 24, "bold"), fg="#2c3e50", bg="#f8f9fa")
        title.pack(pady=(0, 20))
        
        first_label = tk.Label(center_frame, text="Who plays first?", 
                              font=("Arial", 14), fg="#34495e", bg="#f8f9fa")
        first_label.pack(pady=(0, 10))
        
        first_var = tk.StringVar(value="Human")
        tk.Radiobutton(center_frame, text="Human", variable=first_var, 
                      value="Human", font=("Arial", 12), bg="#f8f9fa", fg="#2c3e50").pack()
        tk.Radiobutton(center_frame, text="AI", variable=first_var, 
                      value="AI", font=("Arial", 12), bg="#f8f9fa", fg="#2c3e50").pack()
        
        algo_label = tk.Label(center_frame, text="Select AI Algorithm", 
                             font=("Arial", 14), fg="#34495e", bg="#f8f9fa")
        algo_label.pack(pady=(20, 10))
        
        algo_var = tk.StringVar(value="alphabeta")
        tk.Radiobutton(center_frame, text="Alpha-Beta Pruning", variable=algo_var, 
                      value="alphabeta", font=("Arial", 12), bg="#f8f9fa", fg="#2c3e50").pack()
        tk.Radiobutton(center_frame, text="Minimax", variable=algo_var, 
                      value="minimax", font=("Arial", 12), bg="#f8f9fa", fg="#2c3e50").pack()
        
        start_btn = tk.Label(center_frame, text="Start Game", font=("Arial", 14, "bold"),
                            bg="#27ae60", fg="white", width=15, height=2,
                            cursor="hand2", relief="raised", borderwidth=2)
        start_btn.bind("<Button-1>", lambda e: self.start_hvai_game(first_var.get(), algo_var.get()))
        start_btn.bind("<Enter>", lambda e: e.widget.config(bg="#229954"))
        start_btn.bind("<Leave>", lambda e: e.widget.config(bg="#27ae60"))
        start_btn.pack(pady=30)
        
        back_btn = tk.Label(center_frame, text="Back", font=("Arial", 12),
                            bg="#6c757d", fg="white", width=10, height=1,
                            cursor="hand2", relief="raised", borderwidth=2)
        back_btn.bind("<Button-1>", lambda e: self.show_mode_selection())
        back_btn.bind("<Enter>", lambda e: e.widget.config(bg="#5a6268"))
        back_btn.bind("<Leave>", lambda e: e.widget.config(bg="#6c757d"))
        back_btn.pack()
    
    def show_ai_vs_ai_config(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Main container frame to center content
        main_frame = tk.Frame(self.root, bg="#f8f9fa")
        main_frame.pack(expand=True, fill="both")
        
        # Center frame for content
        center_frame = tk.Frame(main_frame, bg="#f8f9fa")
        center_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        title = tk.Label(center_frame, text="AI vs AI Configuration", 
                        font=("Arial", 24, "bold"), fg="#2c3e50", bg="#f8f9fa")
        title.pack(pady=(0, 20))
        
        ai1_frame = tk.LabelFrame(center_frame, text="AI 1 (X)", font=("Arial", 12, "bold"),
                                 padx=20, pady=15, bg="#f8f9fa", fg="#2c3e50")
        ai1_frame.pack(pady=10, fill="x")
        
        ai1_var = tk.StringVar(value="alphabeta")
        tk.Radiobutton(ai1_frame, text="Alpha-Beta Pruning", variable=ai1_var, 
                      value="alphabeta", font=("Arial", 11), bg="#f8f9fa", fg="#2c3e50").pack(anchor="w")
        tk.Radiobutton(ai1_frame, text="Minimax", variable=ai1_var, 
                      value="minimax", font=("Arial", 11), bg="#f8f9fa", fg="#2c3e50").pack(anchor="w")
        
        ai2_frame = tk.LabelFrame(center_frame, text="AI 2 (O)", font=("Arial", 12, "bold"),
                                 padx=20, pady=15, bg="#f8f9fa", fg="#2c3e50")
        ai2_frame.pack(pady=10, fill="x")
        
        ai2_var = tk.StringVar(value="alphabeta")
        tk.Radiobutton(ai2_frame, text="Alpha-Beta Pruning", variable=ai2_var, 
                      value="alphabeta", font=("Arial", 11), bg="#f8f9fa", fg="#2c3e50").pack(anchor="w")
        tk.Radiobutton(ai2_frame, text="Minimax", variable=ai2_var, 
                      value="minimax", font=("Arial", 11), bg="#f8f9fa", fg="#2c3e50").pack(anchor="w")
        
        start_label = tk.Label(center_frame, text="Who starts?", 
                              font=("Arial", 14), fg="#34495e", bg="#f8f9fa")
        start_label.pack(pady=(10, 5))
        
        first_var = tk.StringVar(value="X")
        tk.Radiobutton(center_frame, text="AI 1 (X)", variable=first_var, 
                      value="X", font=("Arial", 12), bg="#f8f9fa", fg="#2c3e50").pack()
        tk.Radiobutton(center_frame, text="AI 2 (O)", variable=first_var, 
                      value="O", font=("Arial", 12), bg="#f8f9fa", fg="#2c3e50").pack()
        
        start_btn = tk.Label(center_frame, text="Start Game", font=("Arial", 14, "bold"),
                            bg="#27ae60", fg="white", width=15, height=2,
                            cursor="hand2", relief="raised", borderwidth=2)
        start_btn.bind("<Button-1>", lambda e: self.start_aivai_game(ai1_var.get(), 
                                                                      ai2_var.get(), 
                                                                      first_var.get()))
        start_btn.bind("<Enter>", lambda e: e.widget.config(bg="#229954"))
        start_btn.bind("<Leave>", lambda e: e.widget.config(bg="#27ae60"))
        start_btn.pack(pady=20)
        
        back_btn = tk.Label(center_frame, text="Back", font=("Arial", 12),
                            bg="#6c757d", fg="white", width=10, height=1,
                            cursor="hand2", relief="raised", borderwidth=2)
        back_btn.bind("<Button-1>", lambda e: self.show_mode_selection())
        back_btn.bind("<Enter>", lambda e: e.widget.config(bg="#5a6268"))
        back_btn.bind("<Leave>", lambda e: e.widget.config(bg="#6c757d"))
        back_btn.pack()
    
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
        self.game_start_time = datetime.now()
        self.move_number = 0
        
        main_frame = tk.Frame(self.root, bg="#f8f9fa")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        top_frame = tk.Frame(main_frame, bg="#f8f9fa")
        top_frame.pack(fill="x", pady=(0, 15))
        
        title = tk.Label(top_frame, text="Tic-Tac-Toe", 
                        font=("Arial", 20, "bold"), fg="#2c3e50", bg="#f8f9fa")
        title.pack()
        
        content_frame = tk.Frame(main_frame, bg="#f8f9fa")
        content_frame.pack(fill="both", expand=True)
        
        # Left side frame for board and turn label
        left_frame = tk.Frame(content_frame, bg="#f8f9fa")
        left_frame.pack(side="left", padx=(0, 20))
        
        # Turn label above the board
        self.turn_label = tk.Label(left_frame, text=f"Turn: {self.get_player_name()}", 
                                   font=("Arial", 16, "bold"), fg=self.get_turn_color(), bg="#f8f9fa")
        self.turn_label.pack(pady=(0, 10))
        
        board_frame = tk.Frame(left_frame, bg="#f8f9fa")
        board_frame.pack()
        
        self.buttons = []
        for row in range(3):
            button_row = []
            for col in range(3):
                btn = tk.Label(board_frame, text="", font=("Arial", 45, "bold"),
                              width=4, height=2, bg="white", fg="#2c3e50",
                              cursor="hand2", relief="solid", borderwidth=2)
                btn.bind("<Button-1>", lambda e, r=row, c=col: self.make_move(r, c))
                btn.bind("<Enter>", lambda e: e.widget.config(bg="#f8f9fa") if e.widget.cget("text") == "" else None)
                btn.bind("<Leave>", lambda e: e.widget.config(bg="white") if e.widget.cget("text") == "" else None)
                btn.grid(row=row, column=col, padx=2, pady=2)
                button_row.append(btn)
            self.buttons.append(button_row)
        
        # Only show performance metrics for AI games
        if self.game_mode in ["HvAI", "AIvAI"]:
            # Right side frame to center metrics frame
            right_frame = tk.Frame(content_frame, bg="#f8f9fa")
            right_frame.pack(side="right", fill="both", expand=True)
            
            metrics_frame = tk.LabelFrame(right_frame, text="Performance Metrics", 
                                         font=("Arial", 16, "bold"), padx=22, pady=22,
                                         width=320, height=320, bg="#f8f9fa", fg="#2c3e50")
            metrics_frame.place(relx=0.5, rely=0.5, anchor="center")
            metrics_frame.pack_propagate(False)
            
            algo_name = self.get_current_algorithm_name()
            if algo_name:
                self.algo_label = tk.Label(metrics_frame, text=algo_name, 
                                          font=("Arial", 14, "bold"), 
                                          fg="#3498db" if "Alpha-Beta" in algo_name else "#9b59b6",
                                          bg="#f8f9fa")
                self.algo_label.pack(pady=(0, 15))
            else:
                self.algo_label = None
            
            tk.Label(metrics_frame, text="Decision Time:", 
                    font=("Arial", 13), fg="#34495e", bg="#f8f9fa").pack(anchor="w")
            self.time_label = tk.Label(metrics_frame, text="0ms", 
                                       font=("Arial", 13, "bold"), fg="#27ae60", bg="#f8f9fa")
            self.time_label.pack(anchor="w", pady=(0, 15))
            
            tk.Label(metrics_frame, text="Nodes Explored:", 
                    font=("Arial", 13), fg="#34495e", bg="#f8f9fa").pack(anchor="w")
            self.nodes_label = tk.Label(metrics_frame, text="0", 
                                        font=("Arial", 13, "bold"), fg="#2980b9", bg="#f8f9fa")
            self.nodes_label.pack(anchor="w", pady=(0, 15))
            
            tk.Label(metrics_frame, text="Pruning Efficiency:", 
                    font=("Arial", 13), fg="#34495e", bg="#f8f9fa").pack(anchor="w")
            self.pruning_label = tk.Label(metrics_frame, text="N/A", 
                                          font=("Arial", 13, "bold"), fg="#e67e22", bg="#f8f9fa")
            self.pruning_label.pack(anchor="w", pady=(0, 15))
            
            # Export CSV button
            export_btn = tk.Label(metrics_frame, text="Export CSV", font=("Arial", 12),
                                 bg="#3498db", fg="white", width=15, height=2,
                                 cursor="hand2", relief="raised", borderwidth=2)
            export_btn.bind("<Button-1>", lambda e: self.export_game_data())
            export_btn.bind("<Enter>", lambda e: e.widget.config(bg="#2980b9"))
            export_btn.bind("<Leave>", lambda e: e.widget.config(bg="#3498db"))
            export_btn.pack(pady=(10, 0))
        else:
            # For Human vs Human, initialize labels as None to avoid errors
            self.algo_label = None
            self.time_label = None
            self.nodes_label = None
            self.pruning_label = None
        
        # Bottom frame to center buttons vertically in remaining space
        bottom_frame = tk.Frame(main_frame, bg="#f8f9fa")
        bottom_frame.pack(fill="both", expand=True)
        
        # Button container frame centered in bottom space
        button_container = tk.Frame(bottom_frame, bg="#f8f9fa")
        button_container.place(relx=0.5, rely=0.5, anchor="center")
        
        restart_btn = tk.Label(button_container, text="Restart Game", font=("Arial", 14),
                              bg="#f39c12", fg="white", width=15, height=2,
                              cursor="hand2", relief="raised", borderwidth=2)
        restart_btn.bind("<Button-1>", lambda e: self.restart_game())
        restart_btn.bind("<Enter>", lambda e: e.widget.config(bg="#e67e22"))
        restart_btn.bind("<Leave>", lambda e: e.widget.config(bg="#f39c12"))
        restart_btn.pack(side="left", padx=10)
        
        mode_btn = tk.Label(button_container, text="Change Mode", font=("Arial", 14),
                            bg="#95a5a6", fg="white", width=15, height=2,
                            cursor="hand2", relief="raised", borderwidth=2)
        mode_btn.bind("<Button-1>", lambda e: self.change_mode())
        mode_btn.bind("<Enter>", lambda e: e.widget.config(bg="#7f8c8d"))
        mode_btn.bind("<Leave>", lambda e: e.widget.config(bg="#95a5a6"))
        mode_btn.pack(side="left", padx=10)
    
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
    
    def get_turn_color(self):
        return "#e74c3c" if self.current_player == 'X' else "#3498db"
    
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
        self.move_number += 1
        
        # Track move data
        move_data = {
            'game_id': id(self),
            'move_number': self.move_number,
            'player': self.get_player_name(),
            'algorithm': 'Human',
            'position': f'{row},{col}',
            'decision_time_ms': 0,
            'nodes_explored': 0,
            'nodes_pruned': 0,
            'pruning_efficiency': 'N/A'
        }
        self.game_data.append(move_data)
        
        self.update_button(row, col)
        self.root.update()  # Force UI update
        
        if self.check_game_over():
            return
        
        self.current_player = 'O' if self.current_player == 'X' else 'X'
        self.turn_label.config(text=f"Turn: {self.get_player_name()}", fg=self.get_turn_color())
        
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
            self.move_number += 1
            
            # Track move data
            algo_name = self.get_current_algorithm_name()
            pruning_eff = 'N/A'
            if self.ai1_algorithm == "alphabeta" and (self.nodes_explored + self.nodes_pruned) > 0:
                pruning_eff = f"{(self.nodes_pruned / (self.nodes_explored + self.nodes_pruned)) * 100:.1f}%"
            
            move_data = {
                'game_id': id(self),
                'move_number': self.move_number,
                'player': self.get_player_name(),
                'algorithm': algo_name,
                'position': f'{row},{col}',
                'decision_time_ms': f'{self.decision_time:.0f}',
                'nodes_explored': self.nodes_explored,
                'nodes_pruned': self.nodes_pruned,
                'pruning_efficiency': pruning_eff
            }
            self.game_data.append(move_data)
            
            self.update_button(row, col)
            self.update_metrics()
            self.root.update()  # Force UI update
            
            if self.check_game_over():
                return
            
            self.current_player = 'O' if self.current_player == 'X' else 'X'
            self.turn_label.config(text=f"Turn: {self.get_player_name()}", fg=self.get_turn_color())
        
    def update_metrics(self):
        # Only update metrics if labels exist (AI games only)
        if self.time_label:
            self.time_label.config(text=f"{self.decision_time:.0f}ms")
        if self.nodes_label:
            self.nodes_label.config(text=f"{self.nodes_explored}")
        
        # Update algorithm label if it exists
        if self.algo_label:
            algo_name = self.get_current_algorithm_name()
            if algo_name:
                self.algo_label.config(text=algo_name,
                                      fg="#3498db" if "Alpha-Beta" in algo_name else "#9b59b6")
        
        if self.pruning_label:
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
        self.buttons[row][col].config(text=symbol, fg=color)
        self.buttons[row][col].unbind("<Button-1>")
        self.buttons[row][col].unbind("<Enter>")
        self.buttons[row][col].unbind("<Leave>")
    
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
    
    def export_game_data(self):
        if not self.game_data:
            messagebox.showwarning("No Data", "No game data to export!")
            return
        
        # Generate default filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_filename = f"tictactoe_game_{timestamp}.csv"
        
        # Ask user for save location
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialfile=default_filename
        )
        
        if file_path:
            try:
                with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                    fieldnames = ['game_id', 'move_number', 'player', 'algorithm', 'position', 
                                'decision_time_ms', 'nodes_explored', 'nodes_pruned', 'pruning_efficiency']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    
                    writer.writeheader()
                    for move_data in self.game_data:
                        writer.writerow(move_data)
                
                messagebox.showinfo("Export Successful", f"Game data exported to:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Export Error", f"Failed to export data:\n{str(e)}")
    
    def change_mode(self):
        self.reset_game_state()
        self.show_mode_selection()

if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToeUI(root)
    root.mainloop()