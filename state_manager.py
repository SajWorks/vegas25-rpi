from enum import Enum
from typing import Optional
import read_serial

# Create an Enum for the state of the game
class GameState(Enum):
    READY = 1
    PLAY1 = 2
    PLAY2 = 3
    ENDED = 4

# Create a class to represent Player 1's response to Player 2's guess
class GuessResponse:
    def __init__(self, black: int = 0, white: int = 0):
        self.black = black
        self.white = white

# Create a class to represent a guess made by Player 2
class Guess:
    def __init__(self, guess: str, response: Optional[GuessResponse] = None):
        self.guess = guess
        self.response = response

    # Set the response for this guess with the given black and white peg count
    def set_response(self, black: int, white: int) -> None:
        self.response = GuessResponse(black, white)

# Create a class to manage the state of the game
class StateManager:
    def __init__(self):
        # Initialize the game state to READY
        self.state = GameState.READY
        self.guesses: list[Guess] = []
        self.winner: Optional[str] = None
        self.secret_pattern: str = ""

    # Set the state of the game
    def set_state(self, state_value: int):
        try:
            self.state = GameState(state_value)
            print(f"Game state: {self.get_state_name()}")
            if self.state == GameState.PLAY1:
                # Reset button counts when entering PLAY1 state
                read_serial.reset_button_counts()
        except ValueError:
            raise ValueError(f"Invalid state value: {state_value}. Must be 1–4.")

    # Get the current state of the game
    def get_state(self) -> GameState:
        return self.state

    # Get the name of the current state
    def get_state_name(self) -> str:
        return self.state.name

    # Add a new guess to the guesses list and validates it first
    def add_guess(self, guess: str) -> bool:

        # Check if the game is in a valid state to accept guesses
        if self.state not in (GameState.READY, GameState.PLAY2):
            return False

        # Check length
        if len(guess) != 4:
            return False
        
        # Check for valid characters and no duplicates
        valid_chars = set('rgbyop')
        guess_chars = set(guess.lower())
        if not guess_chars.issubset(valid_chars) or len(guess_chars) != 4:
            return False

        # If control reaches this point, the guess is valid.
        # Add the guess and update the game state
        new_guess = Guess(guess)
        self.guesses.append(new_guess)
        self.set_state(GameState.PLAY1)
        return True

    # Set the winner of the game
    def set_winner(self, winner: Optional[str]) -> None:
        self.winner = winner

    # Set the secret pattern for the game
    def set_secret_pattern(self, pattern: str) -> None:
        self.secret_pattern = pattern

    # Handle the end of the input for Player 1's response
    def process_button3_press(self):
        if self.state == GameState.PLAY1 and self.guesses:
            # Get the latest guess
            latest_guess = self.guesses[-1]
            # Set response based on button press counts
            latest_guess.set_response(
                read_serial.button1_presses,
                read_serial.button2_presses
            )
            # Change state to PLAY2 unless the game is over
            if not self.check_game_end():
                self.set_state(GameState.PLAY2.value)

    def check_game_end(self) -> bool:
        """
        Checks if the game should end. Returns True if game should end, False otherwise.
        Game ends if:
        - 10 or more guesses made and last guess wasn't perfect
        - Any guess gets 4 black pegs (perfect guess)
        """
        if not self.guesses:
            return False
            
        latest_guess = self.guesses[-1]
        if not latest_guess.response:
            return False
            
        # Check for perfect guess (4 black pegs)
        if latest_guess.response.black == 4:
            self.set_winner("Player 2")
            self.set_state(GameState.ENDED.value)
            return True
            
        # Check for max guesses reached (10 or more)
        if len(self.guesses) >= 10:
            self.set_winner("Player 1")
            self.set_state(GameState.ENDED.value)
            return True
            
        return False
    
    # Convert the current state to a JSON-compatible dictionary
    def to_json(self) -> dict:
        return {
            "state": self.state.name,
            "guesses": [
                {
                    "guess": g.guess,
                    "response": {
                        "black": g.response.black,
                        "white": g.response.white
                    } if g.response else None
                }
                for g in self.guesses
            ],
            "winner": self.winner,
            "secret_pattern": self.secret_pattern
        }

# Shared instance of StateManager
state_manager = StateManager()