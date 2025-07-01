# server.py
from flask import Flask, jsonify
from flask_cors import CORS
from read_serial import latest_data, start_serial_thread
import write_serial
from pyngrok import ngrok

app = Flask(__name__)
CORS(app)  # Enables CORS for all routes and origins

@app.route('/api/data')
def api_data():
    return jsonify(latest_data)

@app.route('/api/play', methods=['POST'])
def play_note():
    freq = write_serial.write_random_note()
    if freq is not None:
        return jsonify({'status': 'success', 'note': freq}), 200
    else:
        return jsonify({'status': 'error', 'message': 'Serial error'}), 500

if __name__ == '__main__':
    start_serial_thread()

    # Open a public tunnel to the Flask server on port 80
    public_url = ngrok.connect(addr=5000, domain="amazing-crane-ghastly.ngrok-free.app")
    print(" * ngrok tunnel URL:", public_url)
    app.run(port=5000)