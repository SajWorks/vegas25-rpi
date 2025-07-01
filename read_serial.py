# read_serial.py
import serial
import time
import threading

# Shared dictionary to hold latest values
latest_data = {"tempF": None, "tempC": None, "humidity": None}

def parse_data(line):
    try:
        parts = line.strip().split(':')
        tempC = float(parts[0])
        tempF = float(parts[1])
        hum = float(parts[2])
        return tempC, tempF, hum
    except (IndexError, ValueError):
        return None, None, None

def read_serial():
    try:
        ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
        time.sleep(2)  # Wait for Arduino to reset
        while True:
            line = ser.readline().decode('utf-8')
            tempC, tempF, hum = parse_data(line)
            if tempC is not None and tempF is not None and hum is not None:
                latest_data["tempF"] = tempF
                latest_data["tempC"] = tempC
                latest_data["humidity"] = hum
    except serial.SerialException as e:
        print(f"Serial error: {e}")

# Start in background thread
def start_serial_thread():
    thread = threading.Thread(target=read_serial, daemon=True)
    thread.start()