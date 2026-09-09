import random
import os
from datetime import datetime
from typing import Tuple


class GuessGame:
    """Number Guessing Game Class"""
    
    def __init__(self, min_num: int = 1, max_num: int = 100, max_attempts: int = 10):
        """
        Initialize the game
        
        Args:
            min_num: Minimum number in range (default: 1)
            max_num: Maximum number in range (default: 100)
            max_attempts: Maximum guesses allowed (default: 10)
        """
        self.min_num = min_num
        self.max_num = max_num
        self.max_attempts = max_attempts
        self.secret_number = random.randint(min_num, max_num)
        self.attempts = 0
        self.guesses = []
        self.game_won = False
        self.start_time = datetime.now()
    
    def is_valid_guess(self, guess: str) -> Tuple[bool, str]:
        """
        Validate if the guess is a valid number
        
        Args:
            guess: User's input guess
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            num = int(guess)
            if num < self.min_num or num > self.max_num:
                return False, f"Error: Please enter a number between {self.min_num} and {self.max_num}."
            return True, ""
        except ValueError:
            return False, "Error: Please enter a valid number."
    
    def get_hint(self, guess: int) -> str:
        """
        Provide hint based on guess
        
        Args:
            guess: The guessed number
            
        Returns:
            Hint message
        """
        if guess < self.secret_number:
            return " Hint: Your guess is too LOW. Try a higher number!"
        elif guess > self.secret_number:
            return " Hint: Your guess is too HIGH. Try a lower number!"
        else:
            return ""
    
    def make_guess(self, guess_str: str) -> Tuple[bool, str]:
        """
        Process a guess
        
        Args:
            guess_str: The user's guess as string
            
        Returns:
            Tuple of (is_correct, message)
        """
        # Validate input
        is_valid, error_msg = self.is_valid_guess(guess_str)
        if not is_valid:
            return False, error_msg
        
        guess = int(guess_str)
        self.attempts += 1
        self.guesses.append(guess)
        
        # Check if correct
        if guess == self.secret_number:
            self.game_won = True
            return True, self.get_win_message()
        else:
            hint = self.get_hint(guess)
            remaining = self.max_attempts - self.attempts
            return False, f"{hint}\nAttempts remaining: {remaining}/{self.max_attempts}"
    
    def get_win_message(self) -> str:
        """Get victory message with statistics"""
        time_taken = (datetime.now() - self.start_time).total_seconds()
        
        message = f"""
╔══════════════════════════════════════╗
║        CONGRATULATIONS!           ║
║       YOU GUESSED THE NUMBER!        ║
╚══════════════════════════════════════╝

 GAME STATISTICS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ Secret Number: {self.secret_number}
✓ Total Attempts: {self.attempts}
✓ Guesses Made: {self.guesses}
✓ Time Taken: {time_taken:.1f} seconds
✓ Attempts Used: {self.attempts}/{self.max_attempts}

"""
        
        if self.attempts == 1:
            message += " AMAZING! You got it on the first try! You're a genius!\n"
        elif self.attempts <= 3:
            message += " EXCELLENT! You solved it in very few attempts!\n"
        elif self.attempts <= 6:
            message += " GREAT! You found the number efficiently!\n"
        else:
            message += " Good job! You successfully found the number!\n"
        
        return message
    
    def is_game_over(self) -> bool:
        """Check if game is over"""
        return self.game_won or self.attempts >= self.max_attempts
    
    def get_game_status(self) -> str:
        """Get current game status"""
        if self.game_won:
            return "WON"
        elif self.attempts >= self.max_attempts:
            return "LOST"
        else:
            return "PLAYING"
    
    def reveal_answer(self) -> str:
        """Reveal the secret number when game is lost"""
        return f"\n Game Over! The secret number was: {self.secret_number}"
    
    def get_statistics(self) -> dict:
        """Get game statistics"""
        return {
            "attempts": self.attempts,
            "max_attempts": self.max_attempts,
            "guesses": self.guesses,
            "secret_number": self.secret_number,
            "game_won": self.game_won,
            "status": self.get_game_status()
        }


def display_menu():
    """Display main menu"""
    print("\n" + "=" * 50)
    print("       NUMBER GUESSING GAME ".center(50))
    print("=" * 50)
    print("Guess the number between 1 and 100")
    print("You have 10 attempts to find it!")
    print("=" * 50)


def play_game():
    """Main game loop"""
    display_menu()
    game = GuessGame(min_num=1, max_num=100, max_attempts=10)
    
    print("\n I've picked a secret number between 1 and 100.")
    print(" Let's see if you can guess it!\n")
    
    while not game.is_game_over():
        try:
            guess_input = input(f"Attempt {game.attempts + 1}/{game.max_attempts}: Enter your guess: ").strip()
            
            if not guess_input:
                print("Error: Please enter a number!")
                continue
            
            is_correct, message = game.make_guess(guess_input)
            print(message)
            
            if is_correct:
                break
        
        except KeyboardInterrupt:
            print("\n\n Game interrupted by user.")
            print(f"The secret number was: {game.secret_number}")
            return
    
    # Game ended
    if not game.game_won:
        print(game.reveal_answer())
        print("\n Better luck next time!")
    
    # Ask to play again
    play_again = input("\nDo you want to play again? (yes/no): ").strip().lower()
    if play_again in ['yes', 'y']:
        play_game()
    else:
        print("\n Thanks for playing! Goodbye!")


if __name__ == "__main__":
    play_game()