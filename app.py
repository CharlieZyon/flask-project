from flask import Flask, request, jsonify

app = Flask(__name__)

# Store data in a list to preserve old data
data_store = []

# Route to handle POST requests and store the data
@app.route('/', methods=['POST'])
def add_data():
    global data_store

    # Ensure the request contains JSON
    if not request.is_json:
        return jsonify({"error": "Invalid JSON"}), 400

    # Get the JSON data from the request
    new_data = request.get_json()

    # Append the new data to the data_store
    data_store.append(new_data)

    # Return a confirmation response
    return jsonify({"message": "Data added successfully!", "current_data": data_store}), 200

# Route to display the data in the desired format
@app.route('/', methods=['GET'])
def display_data():
    # Prepare the data display format
    formatted_data = []
    for item in data_store:
        formatted_line = (
            f'Product: "{item.get("Product", "N/A")}"  '
            f'ASIN: "{item.get("ASIN", "N/A")}"  '
            f'Country: "{item.get("Country", "N/A")}"  '
            f'IsProduct: "{item.get("IsProduct", "N/A")}"  '
            f'IsCart: "{item.get("IsCart", "N/A")}"'
        )
        formatted_data.append(formatted_line)

    # Join all lines with a newline character
    return "<br>".join(formatted_data), 200

if __name__ == '__main__':
    app.run(debug=True)
