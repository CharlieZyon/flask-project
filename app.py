from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)

# In-memory data store
data_store = []


@app.route('/', methods=['GET'])
def display_data():
    return render_template('index.html', data=data_store)


@app.route('/', methods=['POST'])
def add_data():
    global data_store

    if not request.is_json:
        return jsonify({"error": "Invalid JSON"}), 400

    new_data = request.get_json()
    data_store.append(new_data)

    # Emit the new data to connected clients
    socketio.emit('new_data', new_data)

    return jsonify({"message": "Data added successfully!", "current_data": data_store}), 200


@app.route('/clear', methods=['POST'])
def clear_data():
    global data_store

    data_store = []  # Clear the data store
    socketio.emit('clear_data')  # Notify all clients to clear the table

    return jsonify({"message": "Data cleared successfully!"}), 200


if __name__ == '__main__':
    socketio.run(app, debug=True)
