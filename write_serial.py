import serial
import time

# Define the valid colors for the game
Colors = ["r", "o", "y", "g", "b", "p"]

# This function captures the true pattern from the user input and initializes the game
def initialize_game():
    print("please enter your pattern in this syntax: 'color1,color2,color3,color4'")
    print("Enter your pattern:")
    pattern = input()

    # Ensure the input is a string and split by commas
    TRUE_PATTERN = pattern.replace(",","")

    # Validate the input pattern
    # Call the function to validate the input pattern
    validated_pattern = get_true_pattern(pattern)
    if validated_pattern:
        print("Your pattern is:", validated_pattern)
        print(TRUE_PATTERN)

        # If the pattern is valid, write it to the serial output
        write_true(TRUE_PATTERN)
        return TRUE_PATTERN
    else:
        print("Invalid pattern input.")
        return None

# This function checks if the input pattern is valid
def get_true_pattern(pattern_input):
    try:
        parts = [part.strip().lower() for part in pattern_input.split(',')]
        # Check if the input has exactly 4 colors
        if len(parts) != 4:
            print("Please enter exactly 4 colors separated by commas.")
            return None
        # Validate each color
        for color in parts:
            if color not in Colors:
                print(f"'{color}' is not a valid color. Please use: {', '.join(Colors)}.")
                return None
        for color in parts:
            if parts[0] == parts[1] or parts[0] == parts[2] or parts[0] == parts[3] or parts[1] == parts[2] or parts[1] == parts[3] or parts[2] == parts[3]:
                print("Please enter a pattern with 4 different colors.")
                return None
        # Return the validated pattern as a tuple
        return tuple(parts)

    except serial.SerialException as e:
        print(f"Serial error: {e}")
        return None

def write_true(TRUE_PATTERN):
    try:
        ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
        time.sleep(2)
        command = f"TRUE:{TRUE_PATTERN}\n"
        ser.write(command.encode('utf-8'))
        ser.close()
    except serial.SerialException as e:
        print(f"Serial error: {e}")

def write_guess(GUESS_pattern):
    try:
        ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
        time.sleep(2)
        command = f"GUESS:{GUESS_pattern}\n"
        ser.write(command.encode('utf-8'))
        ser.close()
    except serial.SerialException as e:
        print(f"Serial error: {e}")