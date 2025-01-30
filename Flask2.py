from flask import Flask
app = Flask(__name__)
@app.route('/')
def home():
    return "Hello, Venu"
@app.route('/login', methods=['GET'])
def login():
    username = request.form['username']
    password = request.form['password']
    return f"Username: {username}, Password: {password}"
if __name__ == "__main__":
    app.run(debug=True, port=5008)