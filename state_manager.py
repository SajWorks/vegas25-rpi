from enum import Enum
from typing import Optional

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