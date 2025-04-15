from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask app, SocketIO, and Database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'  # SQLite database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
socketio = SocketIO(app, cors_allowed_origins='*')

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
        socketio.emit('update_data', updated_data)

        return jsonify({"message": "Data added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Clear data route
@app.route('/clear_data', methods=['DELETE'])
def clear_data():
    try:
        # Delete all entries from the database
        db.session.query(ProductData).delete()
        db.session.commit()

        # Emit the empty data list to all connected clients
        socketio.emit('update_data', [])

        return jsonify({"message": "All data cleared successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    socketio.run(app, debug=True)
