# write_serial.py
import serial
import time
import random

# Frequencies of notes in Hz (C4 to B5)
NOTES = [261, 294, 329, 349, 392, 440, 493, 523, 587, 659, 698, 784]

def write_random_note():
    try:
        ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
        time.sleep(2)  # Wait for Arduino to reset
        freq = random.choice(NOTES)
        command = f"BUZZ:{freq}\n"
        ser.write(command.encode('utf-8'))
        print(f"Sent note: {freq} Hz")
        ser.close()
        return freq
    except serial.SerialException as e:
        print(f"Serial error: {e}")
        return None