import logging
from flask import Flask, jsonify, request
import pmsp

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route("/")
def base():
    return "PMSP app", 200

method_cmax = {
        'time': 160.0,
        'gap': 1e-3,
        'print_level': 0,
        'model': 'cmax'
        }

@app.route("/cmax", methods=["POST"])
def solve_cmax():
    instance_json = request.get_json(silent=True)
    if instance_json is None:
        return jsonify({"error": "Invalid or empty JSON provided"}), 400

    try:
        instance = pmsp.load_json(instance_json)
        solution = pmsp.solve_instance(instance, method_cmax)

        return jsonify(solution.set_object()), 200

    except Exception as e:
        logger.exception("An unexpected error occurred during processing")
        return (
            jsonify({"error": "Internal server error processing the instance"}),
            500,
        )

method_et = {
        'time': 160.0,
        'gap': 1e-3,
        'print_level': 0,
        'model': 'sum_e-t'
        }
@app.route('/et', methods=['POST'])

def solve_et():
    instance_json = request.get_json(silent=True)
    if instance_json is None:
        return jsonify({'error': 'Invalid or empty JSON provided'}), 400

    try:
        instance = pmsp.load_json(instance_json)
        solution = pmsp.solve_instance(instance, method_et)

        return jsonify(solution.set_object()), 200

    except Exception as e:
        logger.exception("An unexpected error occurred during processing")
        return (
            jsonify({"error": "Internal server error processing the instance"}),
            500,
        )

if __name__ == "__main__":
    app.run(debug=True)
