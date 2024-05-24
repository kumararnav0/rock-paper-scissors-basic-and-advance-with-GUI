import random
import json

# Define the ASCII art for the moves
basic_moves_art = {
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
'''
}

advanced_moves_art = {
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
       _______
---'   (______)
      (______)
      (____)
---.__(___)
''',
    'SP': '''
       _______
---'   (______)
      (______)
      (_____)
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

def get_user_move(moves):
    while True:
        user_input = input(f"Choose your move ({'/'.join(moves.keys())}) or Q to quit: ").upper()
        if user_input in moves or user_input == 'Q':
            return user_input
        print(f"Invalid input. Please enter {', '.join(moves.keys())}, or Q.")

def get_computer_move(moves):
    return random.choice(list(moves.keys()))

def display_move(move, player, moves_art):
    print(f"{player}'s move:")
    print(moves_art[move])

def play_round(moves, moves_art, outcomes):
    user_move = get_user_move(moves)
    if user_move == 'Q':
        return 'quit', None

    computer_move = get_computer_move(moves)

    display_move(user_move, "Your", moves_art)
    display_move(computer_move, "Opponent's", moves_art)

    result = outcomes[(user_move, computer_move)]
    print(result)
    return result, computer_move

def save_statistics(stats):
    with open("game_stats.json", "w") as file:
        json.dump(stats, file)

def main():
    print("Welcome to the Rock-Paper-Scissors Game!")
    print("You can choose to play either the basic or advanced version of the game.")
    print("In the advanced version, you can also choose Lizard and Spock.")

    game_mode = None

    while game_mode not in ['1', '2']:
        game_mode = input("Choose game mode: \n1 for Basic(Rock, Paper, Scissors)\n2 for Advanced (Rock, Paper, Scissors, Lizard, Spock): ")

    if game_mode == '1':
        moves = basic_moves
        moves_art = basic_moves_art
        outcomes = basic_outcomes
    else:
        moves = advanced_moves
        moves_art = advanced_moves_art
        outcomes = advanced_outcomes

    user_score = 0
    computer_score = 0
    rounds_played = 0
    rounds_to_play = None

    while rounds_to_play is None:
        try:
            rounds_to_play = int(input("Enter the number of rounds you want to play: "))
        except ValueError:
            print("Invalid input. Please enter a number.")

    while rounds_played < rounds_to_play:
        result, computer_move = play_round(moves, moves_art, outcomes)
        if result == 'quit':
            break

        rounds_played += 1

        if "You won" in result:
            user_score += 1
        elif "You lose" in result:
            computer_score += 1

        print(f"Score: You {user_score} - {computer_score} Computer")

    print(f"\nFinal Score after {rounds_played} rounds: You {user_score} - {computer_score} Computer")
    if user_score > computer_score:
        print("Congratulations! You are the overall winner!")
    elif user_score < computer_score:
        print("Better luck next time! The computer wins!")
    else:
        print("It's a draw overall! Well played!")

    stats = {
        "rounds_played": rounds_played,
        "user_score": user_score,
        "computer_score": computer_score
    }
    save_statistics(stats)
    print("Game statistics saved to 'game_stats.json'.")

if __name__ == "__main__":
    main()
