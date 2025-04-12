from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

data_store = []

@app.route('/', methods=['POST'])
def add_data():
    global data_store

    if not request.is_json:
        return jsonify({"error": "Invalid JSON"}), 400

    new_data = request.get_json()
    data_store.append(new_data)

    return jsonify({"message": "Data added successfully!", "current_data": data_store}), 200

@app.route('/', methods=['GET'])
def display_data():
    return render_template('index.html', data=data_store)

if __name__ == '__main__':
    app.run(debug=True)
