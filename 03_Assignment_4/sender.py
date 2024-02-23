# sender.py
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/send_data', methods=['POST'])
def send_data():
    data = request.json.get('data')
    print("Received data:", data)
    # Process data here if needed
    return jsonify({"message": "Data received successfully"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
