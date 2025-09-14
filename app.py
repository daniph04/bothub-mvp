from flask import Flask, request, jsonify


app = Flask(__name__)

# Mock data (MVP)
# These bots are stored in memory; the data resets when the server restarts.
BOTS = [
    {"id": 1, "name": "coinbase-long-bot", "status": "idle"},
    {"id": 2, "name": "bybit-signal-copier", "status": "running"},
]


@app.route("/", methods=["GET"])
def root() -> tuple[dict, int]:
    """
    Health check endpoint for the API root.

    Returns a welcome message in JSON format with a 200 status code.
    """
    return jsonify({"message": "Welcome to BotHub MVP API"}), 200


@app.route("/bots", methods=["GET"])
def list_bots() -> tuple[dict, int]:
    """
    Retrieve the list of bots.

    Returns a JSON object containing a list of example bots and a 200 status code.
    """
    return jsonify({"bots": BOTS}), 200


@app.route("/bots", methods=["POST"])
def create_bot() -> tuple[dict, int]:
    """
    Create a new bot with minimal validation.

    Expects a JSON payload containing at least a 'name' field. The 'status'
    field is optional and defaults to 'idle'. Returns the newly created bot
    and a confirmation message in JSON format with a 201 status code.

    If the 'name' field is missing, returns an error message and a 400
    status code.
    """
    data = request.get_json(silent=True) or {}
    # Minimal validation: ensure the 'name' field is present
    if "name" not in data:
        return jsonify({"error": "Field 'name' is required"}), 400

    # Determine the next available ID
    new_id = max((b["id"] for b in BOTS), default=0) + 1
    bot = {
        "id": new_id,
        "name": data["name"],
        "status": data.get("status", "idle"),
    }
    BOTS.append(bot)
    return jsonify({"message": "Bot created", "bot": bot}), 201


if __name__ == "__main__":
    # Run the Flask development server with debug mode enabled.
    app.run(debug=True)
