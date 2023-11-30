from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import database.db_connector as db

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
    return jsonify({'success': True, 'data': listings})


# Route for searching listings
@app.route('/search', methods=['POST'])
def search_listings():
    search_query = request.json['searchquery']
    db_conn = db.connect_to_database()
    query = """
    SELECT 
        Listings.*, 
        Photos.photoPath
    FROM 
        Listings 
    LEFT JOIN 
        Photos ON Listings.listingID = Photos.listingID
    WHERE 
        Listings.name LIKE %s AND 
        Listings.userID IS NOT NULL AND 
        Listings.endDate >= NOW();
    """
    listings = db.execute_query(db_connection=db_conn, query=query, query_params=(f"%{search_query}%",)).fetchall()
    return jsonify({'success': True, 'data': listings})


# Run listener
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 9991))
    app.run(port=port, debug=True, host='0.0.0.0')
