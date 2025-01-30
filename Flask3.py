from flask import Flask
app = Flask(__name__)
@app.route('/data', methods=['GET'])
def get_data():
    return "This is an example for GET method"

@app.route('/submit', methods=['POST'])
def submit_data():
    data = request.form['key']
    return f"Received: {data}"
@app.route('/update', methods=['PUT'])
def update_data():
    return "This is a PUT request"
@app.route('/example', methods=['GET', 'POST'])
def example():
    if request.method == 'POST':
        return "Handled POST request"
    return "Handled GET request"


if __name__ == "__main__":
    app.run(debug=True, port=5018)
