from flask import Flask, jsonify
import requests
from threading import Lock
from statistics import mean

app = Flask(__name__)

# Configuration
WINDOW_SIZE = 10
NUMBERS_API_URL = "http://localhost:9876/numbers/e" 

numbers = []
lock = Lock()

@app.route('/numbers/<string:numberid>', methods=['GET'])
def get_numbers(numberid):
    if numberid not in ['p', 'f', 'e', 'r']:
        return jsonify({"error": "Invalid number ID"}), 400
    
    with lock:
        window_prev_state = list(numbers)

        try:
            response = requests.get(f"{NUMBERS_API_URL}/{numberid}", timeout=0.5)
            response.raise_for_status()
            new_numbers = response.json()
        except (requests.RequestException, ValueError):
            return jsonify({
                "windowPrevState": window_prev_state,
                "windowCurrState": numbers,
                "numbers": [],
                "avg": calculate_average(numbers)
            }), 200
        
        unique_new_numbers = [num for num in new_numbers if num not in numbers]

        numbers.extend(unique_new_numbers)
        if len(numbers) > WINDOW_SIZE:
            numbers[:] = numbers[-WINDOW_SIZE:]

        return jsonify({
            "windowPrevState": window_prev_state,
            "windowCurrState": numbers,
            "numbers": unique_new_numbers,
            "avg": calculate_average(numbers)
        })

def calculate_average(nums):
    return mean(nums) if nums else 0

if __name__ == '__main__':
    app.run(port=9876)
