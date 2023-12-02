from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import database.db_connector as db
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
from decimal import Decimal, InvalidOperation, ROUND_DOWN
from datetime import datetime

# Set up upload folder
UPLOAD_FOLDER = 'static/img/'

# Initialize Flask app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config.from_mapping(SECRET_KEY='dev')
CORS(app)  # Enable CORS

# Route to display all listings
@app.route('/listings', methods=['GET'])
def get_listings():
    db_conn = db.connect_to_database()

    # Update the query to join the Listings, Photos, and Bids tables
    query = """
    SELECT 
        Listings.*, 
        Photos.photoPath,
        Bids.bidAmt
    FROM 
        Listings 
    LEFT JOIN 
        Photos ON Listings.listingID = Photos.listingID
    LEFT JOIN 
        Bids ON Listings.bidID = Bids.bidID
    WHERE 
        Listings.userID IS NOT NULL AND Listings.endDate >= NOW();
    """

    listings = db.execute_query(db_connection=db_conn, query=query).fetchall()

    processed_listings = []
    for listing in listings:
        processed_listing = {}
        for key, value in listing.items():
            if isinstance(value, Decimal):
                processed_listing[key] = str(value)
            elif isinstance(value, datetime):
                processed_listing[key] = value.strftime('%Y-%m-%d %H:%M')
            else:
                processed_listing[key] = value
        processed_listings.append(processed_listing)
    return jsonify({'success': True, 'data': processed_listings})


# Route for searching listings
@app.route('/search', methods=['POST'])
def search_listings():
    search_query = request.json['searchquery']
    db_conn = db.connect_to_database()
    query = "SELECT * FROM Listings WHERE name LIKE %s AND userID IS NOT NULL AND endDate >= NOW();"
    listings = db.execute_query(db_connection=db_conn, query=query, query_params=(f"%{search_query}%",)).fetchall()
    return jsonify({'success': True, 'data': listings})


@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data['username']
    password = data['password']
    confirm_password = data['confirm_password']
    fname = data['fname']
    lname = data['lname']
    email = data['email']

    db_conn = db.connect_to_database()
    error = None

    if not username or not password or not confirm_password:
        error = 'Username and Password are required.'
    elif password != confirm_password:
        error = 'Passwords do not match.'
    elif db.execute_query(
        db_conn,
        'SELECT userID FROM Users WHERE userName = %s', (username,)
    ).fetchone() is not None:
        error = 'User already registered.'

    if error:
        return jsonify({'success': False, 'error': error}), 400

    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    date_joined = date.today().strftime("%Y-%m-%d")
    rating = 5.0
    isActive = True
    isAdmin = False

    db.execute_query(
        db_conn,
        'INSERT INTO Users (userName, password, firstName, lastName, email, dateJoined, rating, isActive, isAdmin) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)',
        (username, hashed_password, fname, lname, email, date_joined, rating, isActive, isAdmin)
    )

    return jsonify({'success': True, 'message': 'User registered successfully'}), 201


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data['username']
    password = data['password']

    db_conn = db.connect_to_database()
    user = db.execute_query(
        db_conn,
        'SELECT * FROM Users WHERE userName = %s', (username,)
    ).fetchone()

    if user and check_password_hash(user['password'], password):

        return jsonify({'success': True, 'user': {'username': user['userName'], 'email': user['email'], 'id': user['userID']}})

    return jsonify({'success': False, 'error': 'Invalid username or password'}), 401


@app.route('/user/<int:user_id>/profile', methods=['GET'])
def get_user_profile(user_id):
    db_conn = db.connect_to_database()
    user_query = "SELECT * FROM Users WHERE userID = %s;"
    user = db.execute_query(db_connection=db_conn, query=user_query, query_params=(user_id,)).fetchone()


    processed_listing = {}
    for key, value in user.items():
        if isinstance(value, Decimal):
            processed_listing[key] = str(value)
        elif isinstance(value, datetime):
            processed_listing[key] = value.strftime('%Y-%m-%d %H:%M')
        else:
            processed_listing[key] = value

    if not user:
        return jsonify({'success': False, 'error': 'User not found'}), 404

    return jsonify({'success': True, 'data': processed_listing})


@app.route('/user/<int:user_id>/active-listings', methods=['GET'])
def get_active_listings(user_id):
    db_conn = db.connect_to_database()
    listings_query = """
    SELECT 
        Listings.*, 
        Photos.photoPath,
        Bids.bidAmt
    FROM 
        Listings 
    LEFT JOIN 
        Photos ON Listings.listingID = Photos.listingID
    LEFT JOIN 
        Bids ON Listings.bidID = Bids.bidID
    WHERE 
        Listings.userID = %s AND Listings.status = 'active';
    """
    listings = db.execute_query(db_connection=db_conn, query=listings_query, query_params=(user_id,)).fetchall()

    processed_listings = []
    for listing in listings:
        processed_listing = {}
        for key, value in listing.items():
            if isinstance(value, Decimal):
                processed_listing[key] = str(value)
            elif isinstance(value, datetime):
                processed_listing[key] = value.strftime('%Y-%m-%d %H:%M')
            else:
                processed_listing[key] = value
        processed_listings.append(processed_listing)

    return jsonify({'success': True, 'data': processed_listings})


@app.route('/user/<int:user_id>/bid-history', methods=['GET'])
def get_bid_history(user_id):
    db_conn = db.connect_to_database()
    bid_history_query = """
    SELECT 
        Bids.*, 
        Listings.name 
    FROM 
        Bids 
    JOIN 
        Listings ON Bids.listingID = Listings.listingID
    WHERE 
        Bids.userID = %s;
    """
    bid_history = db.execute_query(db_connection=db_conn, query=bid_history_query, query_params=(user_id,)).fetchall()

    processed_listings = []
    for listing in bid_history:
        processed_listing = {}
        for key, value in listing.items():
            if isinstance(value, Decimal):
                processed_listing[key] = str(value)
            elif isinstance(value, datetime):
                processed_listing[key] = value.strftime('%Y-%m-%d %H:%M')
            else:
                processed_listing[key] = value
        processed_listings.append(processed_listing)

    return jsonify({'success': True, 'data': processed_listings})



# Run listener
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 9990))
    app.run(port=port, debug=True, host='0.0.0.0')
