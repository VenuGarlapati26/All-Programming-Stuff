from flask import request, Flask
app = Flask(__name__)

@app.route('/dynamic', methods=['GET', 'POST'])
def dynamic():
    if request.method == 'POST':
        return "This is a POST request"
    return "This is a GET request"
if __name__ == "__main__":
    app.run(debug=True, port=5017)