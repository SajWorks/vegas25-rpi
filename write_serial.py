import serial
Colors = ["r", "o", "y", "g", "b", "p"]
print("please enter your pattern in this syntax: 'color1,color2,color3,color4'")
print("Enter your pattern:")
pattern = input()
TRUE = pattern.replace(",","")


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
        for color in parts:
            if parts[0] == parts[1] or parts[0] == parts[2] or parts[0] == parts[3] or parts[1] == parts[2] or parts[1] == parts[3] or parts[2] == parts[3]:
                print("Please enter a pattern with 4 different colors.")
                return None
    


        return tuple(parts)


    except serial.SerialException as e:
        print(f"Serial error: {e}")
        return None


# Call the function to validate the input pattern
validated_pattern = get_true_pattern(pattern)
if validated_pattern:
    print("Your pattern is:", validated_pattern)

    print(TRUE)
 
else:
    print("Invalid pattern input.")
def write_true():
    try:
        ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
        time.sleep(2)
        command = f"TRUE:{TRUE}\n"
        ser.write(command.encode('utf-8'))
        ser.close()
        print("Pattern sent successfully.")
    except serial.SerialException as e:
        print(f"Serial error: {e}")