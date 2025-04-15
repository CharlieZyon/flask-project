from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask app, SocketIO, and Database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'  # SQLite database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
socketio = SocketIO(app)

# Define the database model
class ProductData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product = db.Column(db.String(255), nullable=True)
    asin = db.Column(db.String(255), nullable=True)
    country = db.Column(db.String(255), nullable=True)
    is_product = db.Column(db.String(255), nullable=True)
    is_cart = db.Column(db.String(255), nullable=True)

# Create the database tables
with app.app_context():
    db.create_all()

# Root route to serve the HTML page
@app.route('/')
def index():
    # Fetch all data from the database to display on the page
    data = ProductData.query.all()
    return render_template('index.html', data=data)

# Add data route
@app.route('/add_data', methods=['POST'])
def add_data():
    try:
        # Get JSON data from the request
        data = request.get_json()

        # Validate the incoming data
        if not data or 'product' not in data or 'asin' not in data or 'country' not in data:
            return jsonify({"error": "Invalid data format"}), 400

        # Save the data to the database
        new_entry = ProductData(
            product=data.get('product'),
            asin=data.get('asin'),
            country=data.get('country'),
            is_product=data.get('isProduct'),
            is_cart=data.get('isCart')
        )
        db.session.add(new_entry)
        db.session.commit()

        # Emit the updated data to all connected clients
        updated_data = [
            {
                "product": entry.product,
                "asin": entry.asin,
                "country": entry.country,
                "isProduct": entry.is_product,
                "isCart": entry.is_cart
            }
            for entry in ProductData.query.all()
        ]
        socketio.emit('update_data', updated_data, namespace='/')

        return jsonify({"message": "Data added successfully!"}), 200

    except Exception as e:
        # Log the error for debugging
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

# Clear data route
@app.route('/clear_data', methods=['POST'])
def clear_data():
    try:
        # Delete all data from the database
        db.session.query(ProductData).delete()
        db.session.commit()

        # Emit an empty data set to all connected clients
        socketio.emit('update_data', [], namespace='/')

        return jsonify({"message": "All data cleared!"}), 200

    except Exception as e:
        # Log the error for debugging
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

# Test route to ensure the server is working
@app.route('/test', methods=['GET'])
def test():
    return jsonify({"message": "Server is working!"}), 200

if __name__ == '__main__':
    # Run the app with SocketIO
    socketio.run(app, host='0.0.0.0', port=5001)
