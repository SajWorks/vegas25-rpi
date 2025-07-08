from enum import Enum

# Create an Enum for the state of the game
class GameState(Enum):
    READY = 1
    PLAY1 = 2
    PLAY2 = 3
    ENDED = 4

# Create a class to manage the state of the game
class StateManager:
    def __init__(self):
        # Initialize the game state to READY
        self.state = GameState.READY

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