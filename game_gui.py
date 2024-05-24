import tkinter as tk
from tkinter import messagebox
import random
import json

# Define the ASCII art for the moves with better design
moves_art = {
    'R': '''
    _______
---'   ____)
      (_____)
      (_____)
      (____)
---.__(___)
''',
    'P': '''
     _______
---'    ____)____
           ______)
          _______)
         _______)
---.__________)
''',
    'S': '''
    _______
---'   ____)____
          ______)
       __________)
      (____)
---.__(___)
''',
    'L': '''
      ____
---'  (____)
     (______)
     (______)
      (____)
---.__(___)
''',
    'SP': '''
      _____
---'  ____)____
          ______)
       __________)
      (____)
---.__(___)
'''
}

# Define the mapping for moves
basic_moves = {
    'R': 'Rock',
    'P': 'Paper',
    'S': 'Scissors'
}

advanced_moves = {
    'R': 'Rock',
    'P': 'Paper',
    'S': 'Scissors',
    'L': 'Lizard',
    'SP': 'Spock'
}

# Define the outcomes with detailed descriptions
basic_outcomes = {
    ('R', 'R'): "It's a draw",
    ('R', 'P'): "Paper covers Rock. You lose",
    ('R', 'S'): "Rock crushes Scissors. You won",
    ('P', 'R'): "Paper covers Rock. You won",
    ('P', 'P'): "It's a draw",
    ('P', 'S'): "Scissors cuts Paper. You lose",
    ('S', 'R'): "Rock crushes Scissors. You lose",
    ('S', 'P'): "Scissors cuts Paper. You won",
    ('S', 'S'): "It's a draw"
}

advanced_outcomes = {
    ('R', 'R'): "It's a draw",
    ('R', 'P'): "Paper covers Rock. You lose",
    ('R', 'S'): "Rock crushes Scissors. You won",
    ('R', 'L'): "Rock crushes Lizard. You won",
    ('R', 'SP'): "Spock vaporizes Rock. You lose",
    ('P', 'R'): "Paper covers Rock. You won",
    ('P', 'P'): "It's a draw",
    ('P', 'S'): "Scissors cuts Paper. You lose",
    ('P', 'L'): "Lizard eats Paper. You lose",
    ('P', 'SP'): "Paper disproves Spock. You won",
    ('S', 'R'): "Rock crushes Scissors. You lose",
    ('S', 'P'): "Scissors cuts Paper. You won",
    ('S', 'S'): "It's a draw",
    ('S', 'L'): "Scissors decapitates Lizard. You won",
    ('S', 'SP'): "Spock smashes Scissors. You lose",
    ('L', 'R'): "Rock crushes Lizard. You lose",
    ('L', 'P'): "Lizard eats Paper. You won",
    ('L', 'S'): "Scissors decapitates Lizard. You lose",
    ('L', 'L'): "It's a draw",
    ('L', 'SP'): "Lizard poisons Spock. You won",
    ('SP', 'R'): "Spock vaporizes Rock. You won",
    ('SP', 'P'): "Paper disproves Spock. You lose",
    ('SP', 'S'): "Spock smashes Scissors. You won",
    ('SP', 'L'): "Lizard poisons Spock. You lose",
    ('SP', 'SP'): "It's a draw"
}

class RPSLSGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Rock-Paper-Scissors-Lizard-Spock Game")
        self.root.configure(bg='#222831')
        
        self.user_score = 0
        self.computer_score = 0
        self.rounds_played = 0
        self.rounds_to_play = tk.IntVar(value=5)
        self.mode = tk.StringVar(value="basic")
        
        self.frames = {}
        self.create_frames()
        self.show_frame("WelcomeScreen")
    
    def create_frames(self):
        for F in (WelcomeScreen, ModeSelectionScreen, RoundSelectionScreen, GameScreen):
            page_name = F.__name__
            frame = F(parent=self.root, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
    
    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def play_round(self, user_move):
        if self.mode.get() == "basic":
            moves = list(basic_moves.keys())
            outcomes = basic_outcomes
        else:
            moves = list(advanced_moves.keys())
            outcomes = advanced_outcomes
        
        computer_move = random.choice(moves)
        
        self.frames["GameScreen"].display_moves(user_move, computer_move)
        
        result = outcomes[(user_move, computer_move)]
        self.frames["GameScreen"].result_label.config(text=result, bg="#EEEEEE")
        
        if "You won" in result:
            self.user_score += 1
        elif "You lose" in result:
            self.computer_score += 1
        
        self.rounds_played += 1
        
        self.frames["GameScreen"].update_score()
        
        if self.rounds_played >= self.rounds_to_play.get():
            self.end_game()
    
    def reset_game(self):
        self.user_score = 0
        self.computer_score = 0
        self.rounds_played = 0
        self.rounds_to_play.set(5)
        self.frames["GameScreen"].update_score()
        self.frames["GameScreen"].result_label.config(text="", bg="#393E46")
        self.frames["GameScreen"].user_move_label.config(text="", bg="#393E46")
        self.frames["GameScreen"].computer_move_label.config(text="", bg="#393E46")
    
    def end_game(self):
        if self.user_score > self.computer_score:
            messagebox.showinfo("Game Over", "Congratulations! You are the overall winner!")
        elif self.user_score < self.computer_score:
            messagebox.showinfo("Game Over", "Better luck next time! The computer wins!")
        else:
            messagebox.showinfo("Game Over", "It's a draw overall! Well played!")
        
        self.save_statistics()
        self.prompt_next_action()
    
    def save_statistics(self):
        stats = {
            "rounds_played": self.rounds_played,
            "user_score": self.user_score,
            "computer_score": self.computer_score
        }
        with open("game_stats.json", "w") as file:
            json.dump(stats, file)
        messagebox.showinfo("Game Statistics", "Game statistics saved to 'game_stats.json'.")
    
    def prompt_next_action(self):
        response = messagebox.askyesno("Next Action", "Do you want to add more rounds?")
        if response:
            self.add_rounds()
        else:
            self.reset_game()
            self.show_frame("WelcomeScreen")
    
    def add_rounds(self):
        rounds = tk.simpledialog.askinteger("Add Rounds", "Enter the number of additional rounds:")
        if rounds:
            self.rounds_to_play.set(self.rounds_to_play.get() + rounds)
            self.show_frame("GameScreen")
            self.frames["GameScreen"].update_score()
        else:
            self.reset_game()
            self.show_frame("WelcomeScreen")

class WelcomeScreen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg='#222831')
        
        label = tk.Label(self, text="Welcome to the Rock-Paper-Scissors-Lizard-Spock Game!", font=("Helvetica", 16, 'bold'), bg='#00ADB5', fg='#EEEEEE', padx=10, pady=10)
        label.pack(pady=10, fill=tk.X)
        
        start_button = tk.Button(self, text="Start", command=lambda: controller.show_frame("ModeSelectionScreen"), font=("Helvetica", 12), bg="#00ADB5", fg="#EEEEEE", activebackground='#00ADB5', relief=tk.RAISED, bd=5)
        start_button.pack(pady=10)

class ModeSelectionScreen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg='#222831')
        
        label = tk.Label(self, text="Choose game mode:", font=("Helvetica", 16, 'bold'), bg='#00ADB5', fg='#EEEEEE', padx=10, pady=10)
        label.pack(pady=10, fill=tk.X)
        
        basic_button = tk.Button(self, text="Basic (Rock, Paper, Scissors)", command=lambda: self.set_mode("basic"), font=("Helvetica", 12), bg="#393E46", fg="#EEEEEE", activebackground='#393E46', relief=tk.RAISED, bd=5)
        basic_button.pack(pady=10)
        
        advanced_button = tk.Button(self, text="Advanced (Rock, Paper, Scissors, Lizard, Spock)", command=lambda: self.set_mode("advanced"), font=("Helvetica", 12), bg="#393E46", fg="#EEEEEE", activebackground='#393E46', relief=tk.RAISED, bd=5)
        advanced_button.pack(pady=10)
        
    def set_mode(self, mode):
        self.controller.mode.set(mode)
        self.controller.frames["GameScreen"].setup_buttons(mode)
        self.controller.show_frame("RoundSelectionScreen")

class RoundSelectionScreen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg='#222831')
        
        label = tk.Label(self, text="Enter the number of rounds you want to play:", font=("Helvetica", 16, 'bold'), bg='#00ADB5', fg='#EEEEEE', padx=10, pady=10)
        label.pack(pady=10, fill=tk.X)
        
        self.rounds_entry = tk.Entry(self, textvariable=controller.rounds_to_play, font=("Helvetica", 12), width=5)
        self.rounds_entry.pack(pady=10)
        
        start_game_button = tk.Button(self, text="Start Game", command=lambda: controller.show_frame("GameScreen"), font=("Helvetica", 12), bg="#00ADB5", fg="#EEEEEE", activebackground='#00ADB5', relief=tk.RAISED, bd=5)
        start_game_button.pack(pady=10)

class GameScreen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg='#393E46')
        
        self.result_label = tk.Label(self, text="", font=("Helvetica", 14), bg='#393E46', fg='#EEEEEE')
        self.result_label.pack(pady=10)
        
        self.score_label = tk.Label(self, text=f"Score: You 0 - 0 Computer", font=("Helvetica", 14), bg='#393E46', fg='#EEEEEE')
        self.score_label.pack(pady=10)
        
        self.moves_frame = tk.Frame(self, bg='#393E46')
        self.moves_frame.pack(pady=10)

        self.user_move_label = tk.Label(self.moves_frame, text="", font=("Helvetica", 12), bg='#393E46', fg='#EEEEEE')
        self.user_move_label.pack(side=tk.LEFT, padx=20)

        self.computer_move_label = tk.Label(self.moves_frame, text="", font=("Helvetica", 12), bg='#393E46', fg='#EEEEEE')
        self.computer_move_label.pack(side=tk.LEFT, padx=20)
        
        self.buttons_frame = tk.Frame(self, bg='#393E46')
        self.buttons_frame.pack(pady=10)
        
        self.move_buttons = []

    def setup_buttons(self, mode):
        for btn in self.move_buttons:
            btn.destroy()

        self.move_buttons.clear()
        
        moves = basic_moves if mode == "basic" else advanced_moves
        for move in moves.keys():
            btn = tk.Button(self.buttons_frame, text=moves[move], command=lambda m=move: self.controller.play_round(m), width=12, height=5, bg='#00ADB5', fg='#EEEEEE', activebackground='#00ADB5', relief=tk.RAISED, bd=5)
            btn.pack(side=tk.LEFT, padx=5)
            self.move_buttons.append(btn)
        
    def display_moves(self, user_move, computer_move):
        moves = basic_moves if self.controller.mode.get() == "basic" else advanced_moves
        self.user_move_label.config(text=f"Your move:\n{moves[user_move]}\n{moves_art[user_move]}")
        self.computer_move_label.config(text=f"Computer's move:\n{moves[computer_move]}\n{moves_art[computer_move]}")
    
    def update_score(self):
        self.score_label.config(text=f"Score: You {self.controller.user_score} - {self.controller.computer_score} Computer")

def main():
    root = tk.Tk()
    game = RPSLSGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()
