from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager, create_access_token,
    jwt_required, get_jwt_identity
)
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__, static_folder="../frontend/dist", static_url_path="/")

CORS(app)

app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "super-secret-key")

jwt = JWTManager(app)

users = []

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    for user in users:
        if user["username"] == username:
            return jsonify({"message": "User already exists"}), 400
    users.append({"username": username, "password": password})
    return jsonify({"message": "User registered successfully"}), 201

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    for user in users:
        if user["username"] == username and user["password"] == password:
            access_token = create_access_token(identity=username)
            return jsonify({"access_token": access_token})
    return jsonify({"message": "Invalid username or password"}), 401

@app.route("/dashboard", methods=["GET"])
@jwt_required()
def dashboard():
    current_user = get_jwt_identity()
    return jsonify({"message": f"Welcome {current_user} to dashboard"})

# Sert le frontend React pour toutes les autres routes
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve(path):
    if path and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, "index.html")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)