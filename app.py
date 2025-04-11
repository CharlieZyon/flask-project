from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Store default parameter values
parameters = {
    "Product": "None",
    "ASIN": "None",
    "Country": "None",
    "IsProduct": "None",
    "IsCart": "None"
}

@app.route("/", methods=["GET", "POST"])
def home():
    global parameters

    # Handle POST request to update parameters
    if request.method == "POST":
        if request.is_json:
            data = request.get_json()
            parameters["Product"] = data.get("Product", parameters["Product"])
            parameters["ASIN"] = data.get("ASIN", parameters["ASIN"])
            parameters["Country"] = data.get("Country", parameters["Country"])
            parameters["IsProduct"] = data.get("IsProduct", parameters["IsProduct"])
            parameters["IsCart"] = data.get("IsCart", parameters["IsCart"])
            return jsonify({"message": "Parameters updated successfully!", "parameters": parameters}), 200
        else:
            return jsonify({"error": "Invalid content type! Please use application/json."}), 400

    # Render the HTML page
    return render_template("index.html", parameters=parameters)

if __name__ == "__main__":
    app.run(debug=True)
