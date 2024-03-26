from flask import Flask, request, jsonify
import re
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config["MONGO_URI"] = "mongodb://localhost:27017/foodcourt"
mongo = PyMongo(app).db


def validate_user_data(user_data):
    """
    Validates user registration data:
        - Checks for missing required fields.
        - Validates email format using regular expression.
        - Checks for duplicate email addresses.
    """
    required_fields = {"name", "email", "password"}
    missing_fields = required_fields - set(user_data.keys())
    if missing_fields:
        return jsonify({"error": f"Missing required fields: {', '.join(missing_fields)}"}), 400

    if not re.match(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', user_data["email"]):
        return jsonify({"error": "Invalid email format"}), 400

    if mongo.users_collection.find_one({"email": user_data["email"]}):
        return jsonify({"error": "Email address already in use"}), 400

    return None


@app.route("/api/signup", methods=["POST"])
def signup():
    user_data = request.get_json()

    validation_error = validate_user_data(user_data)
    if validation_error:
        return validation_error

    hashed_password = generate_password_hash(user_data["password"])

    user = {"name": user_data["name"], "email": user_data["email"], "password": hashed_password}

    try:
        mongo.users_collection.insert_one(user)
        return jsonify({"message": "User created successfully!"}), 201
    except Exception as e:  # Catch potential MongoDB errors
        print(f"Error creating user: {e}")
        return jsonify({"error": "An error occurred during user creation"}), 500


@app.route("/api/login", methods=["POST"])
def login():
    user_data = request.get_json()

    if not user_data or not user_data.get("email") or not user_data.get("password"):
        return jsonify({"error": "Missing username or password"}), 400

    email = user_data["email"]
    password = user_data["password"]

    user = mongo.users_collection.find_one({"email": email})

    if not user:
        return jsonify({"error": "Invalid email or password"}), 401

    if not check_password_hash(user["password"], password):
        return jsonify({"error": "Invalid email or password"}), 401

    return jsonify({"message": "Login successful!"}), 200


@app.route("/api/canteen")
def get_canteen():
    """
    Retrieves all canteens from the "canteen_collection"
    """
    canteens = mongo.canteen_collection.find({})
    return jsonify([{"name": canteen["name"]} for canteen in canteens]), 200


@app.route("/api/food", methods=["POST"])
def get_food():
    """
    Retrieves food items based on the provided canteen name in the request body.
    Expects JSON data with a "canteen" field.
    """
    data = request.get_json()
    if not data or not data.get("canteen"):
        return jsonify({"error": "Missing required field: canteen"}), 400

    foods = mongo.food_collection.find({"canteen": data["canteen"]})
    final_foods = []
    for food in foods:
        final_foods.append({"name": food["name"], "price": food["price"]})
    return jsonify(final_foods), 200


if __name__ == "__main__":
    app.run(debug=True)
