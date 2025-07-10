# server.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import read_serial
import write_serial
from pyngrok import ngrok
from state_manager import state_manager, Guess, GuessResponse

app = Flask(__name__)
CORS(app)  # Enables CORS for all routes and origins

# Create a state manager instance
# state_manager = StateManager()

@app.route('/api/data')
def api_data():
    return jsonify({'button1': read_serial.button1_presses,
                    'button2': read_serial.button2_presses,
                    'button3': read_serial.button3_presses}), 200

@app.route('/api/game_state', methods=['GET'])
def get_current_state():
    return jsonify(state_manager.to_json()), 200

@app.route('/api/guess', methods=['POST'])
def submit_guess():
    guess = request.args.get('guess')
    
    if guess is None:
        return jsonify({
            'status': 'error',
            'message': 'No guess provided in url parameters'
        }), 400
    
    try:
        # Validate the guess length and characters
        if not state_manager.add_guess(guess):
            return jsonify({
                'status': 'error',
                'message': 'Invalid guess'
            }), 400

        # Write the guess to the serial port
        write_serial.write_guess(guess)   
        return jsonify({
            'status': 'success',
            'guess': guess
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400

@app.route('/api/set_state', methods=['POST'])
def set_state():
    state = request.args.get('state')

    if state is None:
        return jsonify({
            'status': 'error',
            'message': 'No state provided in url parameters'
        }), 400
        
    try:
        state_manager.set_state(int(state))
        return jsonify({
            'status': 'success',
            'state': state_manager.get_state_name()
        })
    except ValueError as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400

def start_server():
    read_serial.start_serial_thread()
    public_url = ngrok.connect(addr=5000, domain="amazing-crane-ghastly.ngrok-free.app")
    print(" * ngrok tunnel URL:", public_url)
    app.run(port=5000)

if __name__ == "__main__":

    # Try to initialize the game
    true_pattern = write_serial.initialize_game()
    if not true_pattern:
        print("Failed to initialize the game. Exiting.")
        exit(1)
    else:
        # Set the secret pattern in the state manager
        state_manager.set_secret_pattern(true_pattern)

        # Print the initial state of the game
        print(f"Initial game state: {state_manager.get_state_name()}")

        # Start the Flask server with ngrok tunnel
        start_server()

    