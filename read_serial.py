# read_serial.py
import serial
import time
import threading
from state_manager import state_manager

# Shared dictionary to hold latest values
latest_data = {"tempF": None, "tempC": None, "humidity": None}
button1_presses = 0
button2_presses = 0
button3_presses = 0

def reset_button_counts():  
    global button1_presses, button2_presses, button3_presses
    button1_presses = 0
    button2_presses = 0
    button3_presses = 0

def parse_data(line):
    try:
        # Check for button presses like "Button: 1"
        button1_pressed = 0
        button2_pressed = 0
        button3_pressed = 0
        stripped_line = line.strip()
        if stripped_line == "Button: 1":
            print("Button 1 pressed")
            button1_pressed = 1
        elif stripped_line == "Button: 2":
            print("Button 2 pressed")
            button2_pressed = 1
        elif stripped_line == "Button: 3":
            print("Button 3 pressed")
            button3_pressed = 1
        return button1_pressed, button2_pressed, button3_pressed
    except (IndexError, ValueError):
        return 0, 0, 0

def read_serial():
    try:
        ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
        time.sleep(2)  # Wait for Arduino to reset
        while True:
            line = ser.readline().decode('utf-8')
            button1_pressed, button2_pressed, button3_pressed = parse_data(line)
            global button1_presses, button2_presses, button3_presses
            button1_presses += button1_pressed
            button2_presses += button2_pressed
            button3_presses += button3_pressed

            # If button 3 was pressed, notify state manager
            if button3_pressed:
                state_manager.process_button3_press()
    except serial.SerialException as e:
        print(f"Serial error: {e}")

# Start in background thread
def start_serial_thread():
    thread = threading.Thread(target=read_serial, daemon=True)
    thread.start()