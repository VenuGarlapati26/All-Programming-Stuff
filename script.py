from flask import Flask, jsonify, request
app = Flask(__name__)
users = [{"id": 1, "name": "venu", "email": "venu@indwes.com"}, {"id":2, "name": "gopi", "email": "gopi@thermax.com"}]

@app.route("/")
def home():
    return "Welcome to the API"

@app.route("/users", methods=["GET"])
def get_users():
    return jsonify(users)

@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = next((u for u in users if u["id"] == user_id), None)
    if user:
        return jsonify(user)
    return jsonify({"error": "user not found"}), 404

@app.route("/users", methods=["POST"])
def add_user():
    data = request.json
    new_user = {"id": len(users) + 1, "name": data["name"], "email": data["email"]}
    users.append(new_user)
    return jsonify(new_user), 201

@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.json
    user = next((u for u in users if u["id"] == user_id), None)
    if user:
        user.update(data)
        return jsonify(user)
    return jsonify({"error": "user not found"}), 404

@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    global users
    users = [u for u in users if u["id"] != user_id]
    return jsonify({"message": "user deleted"}), 200

if __name__ == "__main__":
    app.run(debug=True)