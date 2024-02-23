# receiver.py
from flask import Flask, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('receiver.html')

@app.route('/get_data', methods=['GET'])
def get_data():
    # Replace this with the data you want to send
    data = "Hello from sender!"
    return jsonify({"data": data})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
