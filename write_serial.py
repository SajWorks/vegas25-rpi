import serial
Colors = ["red", "orange", "yellow", "green", "blue", "purple"]
print("please enter your pattern in this syntax: 'color1, color2, color3', color4'")
print("Enter your pattern:")
pattern = input()

def get_true_pattern(pattern_input):
    try:
        parts = [part.strip().lower() for part in pattern_input.split(',')]
        if len(parts) != 4:
            print("Please enter exactly 4 colors separated by commas.")
            return None

        # Validate each color
        for color in parts:
            if color not in Colors:
                print(f"'{color}' is not a valid color. Please use: {', '.join(Colors)}.")
                return None

        return tuple(parts)

    except serial.SerialException as e:
        print(f"Serial error: {e}")
        return None

# Call the function to validate the input pattern
validated_pattern = get_true_pattern(pattern)
if validated_pattern:
    print("Your pattern is:", validated_pattern)
else:
    print("Invalid pattern input.")