from flask import Flask, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('receiver.html')

@app.route('/get_data', methods=['GET'])
def get_data():
    conversation = ["Goodbye", "Yes, it is indeed nice to meet you."]
    data = ["token",conversation[0]]
    return jsonify({"data": data})

if __name__ == '__main__':
    app.run(host='192.0.0.2', port=80)
