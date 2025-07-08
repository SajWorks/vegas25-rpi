# server.py
from flask import Flask, jsonify
from flask_cors import CORS
import read_serial
import write_serial
from pyngrok import ngrok

app = Flask(__name__)
CORS(app)  # Enables CORS for all routes and origins

@app.route('/api/data')
def api_data():
    return jsonify({'button1': read_serial.button1_presses,
                    'button2': read_serial.button2_presses,
                    'button3': read_serial.button3_presses}), 200

@app.route('/api/play', methods=['POST'])
def play_note():
    TRUE = write_serial.write_true()
    if TRUE is not None:
        return jsonify({'status': 'success', 'note': TRUE}), 200
    else:
        return jsonify({'status': 'error', 'message': 'Serial error'}), 500

if __name__ == '__main__':
    read_serial.start_serial_thread()
    public_url = ngrok.connect(addr=5000, domain="amazing-crane-ghastly.ngrok-free.app")
    print(" * ngrok tunnel URL:", public_url)
    app.run(port=5000)