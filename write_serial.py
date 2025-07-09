import serial
import time
Colors = ["r", "o", "y", "g", "b", "p"]
print("please enter your pattern in this syntax: 'color1,color2,color3,color4'")
print("Enter your pattern:")
pattern = input()
# Validate the input pattern
# Ensure the input is a string and split by commas
TRUE = pattern.replace(",","")
GUESS_pattern = input("Enter your guess: ")
GUESS = GUESS_pattern.replace(",", "")
# Function to validate the guess pattern
# This function checks if the input pattern is valid
def get_guess_pattern(GUESS_pattern):
    try:
        parts = [part.strip().lower() for part in GUESS_pattern.split(',')]
       
        if len(parts) != 4:
            print("Please enter exactly 4 colors separated by commas.")
            return None
        # Validate each color
        for color in parts:
            if color not in Colors:
                print(f"'{color}' is not a valid color. Please use: {', '.join(Colors)}.")
                return None
            # Check for duplicates
        for color in parts:
            if parts[0] == parts[1] or parts[0] == parts[2] or parts[0] == parts[3] or parts[1] == parts[2] or parts[1] == parts[3] or parts[2] == parts[3]:
                print("Please enter a pattern with 4 different colors.")
                return None
        return tuple(parts)


    except serial.SerialException as e:
        print(f"Serial error: {e}")
        return None
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
#    except ValueError:
    except serial.SerialException as e:
        print(f"Serial error: {e}")
        return None
# Validate the guess pattern
# Call the function to validate the input pattern
validated_pattern = get_true_pattern(pattern)
if validated_pattern:
    print("Your pattern is:", validated_pattern)
    print(TRUE)
    print("your guess is:", GUESS_pattern)
    print(GUESS)
else:
    print("Invalid pattern input.")
def write_true():
    try:
        ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
        time.sleep(2)
        command = f"TRUE:{TRUE}\n"
        ser.write(command.encode('utf-8'))
        print(command)
        ser.close()
    except serial.SerialException as e:
        print(f"Serial error: {e}")
def write_guess():
    try:
        ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
        time.sleep(2)
        command = f"GUESS:{GUESS_pattern}\n"
        ser.write(command.encode('utf-8'))
        print(command)
        ser.close()
    except serial.SerialException as e:
        print(f"Serial error: {e}")

write_guess()
write_true()