from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

# Store data in memory (for simplicity; in production, use a database)
data_store = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_data', methods=['POST'])
def add_data():
    global data_store
    new_data = request.json
    data_store.append(new_data)
    socketio.emit('update_data', data_store, broadcast=True)  # Broadcast to all clients
    return jsonify({"message": "Data added successfully!"}), 200

@app.route('/clear_data', methods=['POST'])
def clear_data():
    global data_store
    data_store = []
    socketio.emit('clear_data', broadcast=True)  # Notify all clients to clear data
    return jsonify({"message": "Data cleared successfully!"}), 200

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5001)
