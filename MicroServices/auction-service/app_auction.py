from flask import Flask, render_template, request, redirect, g, url_for, flash,jsonify
import os
import database.db_connector as db
from flask_cors import CORS
# from datetime import date
from werkzeug.utils import secure_filename
from validation import validate_new_listing, validate_photo, validate_bid
import threading
# from datetime import datetime
import datetime

# Set up upload folder
UPLOAD_FOLDER = 'static/img/'

# Initialize Flask app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config.from_mapping(SECRET_KEY='dev')
CORS(app)  # Enable CORS

# The function for keep looping and check the status of the listings
def update_listing_status():
    while True:
        current_time = datetime.datetime.now()
        db_conn = db.connect_to_database()

        # Update listings to 'active' if current time is equal to startDate
        update_query = """
        UPDATE Listings 
        SET status = 'active' 
        WHERE startDate <= %s AND endDate > %s AND status != 'active';
        """
        db.execute_query(db_connection=db_conn, query=update_query, query_params=(current_time, current_time))

        # Update listings to 'hold' if current time is greater than or equal to endDate
        update_query = """
        UPDATE Listings 
        SET status = 'hold' 
        WHERE endDate <= %s AND status != 'hold';
        """
        db.execute_query(db_connection=db_conn, query=update_query, query_params=(current_time,))
        
        # Update countdown for active listings
        update_query = """
        UPDATE Listings 
        SET countDown = TIMESTAMPDIFF(SECOND, %s, endDate) 
        WHERE endDate > %s AND status = 'active';
        """
        db.execute_query(db_connection=db_conn, query=update_query, query_params=(current_time, current_time))

        # Sleep for 1 second before the next check, maybe we can change to 60s
        time.sleep(1)

# Start the thread
update_thread = threading.Thread(target=update_listing_status)
update_thread.start()


@app.route('/', methods=['GET', 'POST'])
def root():
    db_conn = db.connect_to_database()

    query = "SELECT bidID, bidAmt FROM Bids;"
    bids = db.execute_query(db_connection=db_conn, query=query).fetchall()

    query = "SELECT listingID, photoPath FROM Photos;"
    photos = db.execute_query(
        db_connection=db_conn, query=query).fetchall()

    if request.method == 'GET':
        query = "SELECT * FROM Listings WHERE userID IS NOT NULL AND expirationDate >= NOW();"
        listings = db.execute_query(
            db_connection=db_conn, query=query).fetchall()

    elif request.method == 'POST':
        search_query = f"%{request.form['searchquery']}%"
        query = "SELECT * FROM Listings WHERE name LIKE %s AND userID IS NOT NULL AND expirationDate >= NOW();"
        listings = db.execute_query(db_connection=db_conn, query=query,
                                    query_params=(search_query,)).fetchall()

    return render_template('main.j2', listings=listings, bids=bids, photos=photos)


@app.route('/place-bid/<int:list_id>', methods=['GET', 'POST'])
def place_bid(list_id):
    if request.method == 'POST':
        bid_amt = int(request.form['bid'])
        bid_date = date.today()
        db_conn = db.connect_to_database()

        query = "SELECT l.listingID, l.bidID, l.startPrice as startPrice, b.bidAmt as amount FROM Listings l LEFT JOIN Bids b ON l.bidID = b.bidID WHERE l.listingID = %s;"
        high_bid = db.execute_query(db_connection=db_conn, query=query,
                                    query_params=(list_id,)).fetchone()

        valid_bid, message = validate_bid(bid_amt, high_bid)
        if not valid_bid:
            flash(message, 'danger')
            return redirect(url_for('root'))
        else:
            query = "INSERT INTO Bids (userID, listingID, bidAmt, bidDate) VALUES (%s, %s, %s, %s)"
            cursor = db.execute_query(db_connection=db_conn, query=query,
                                      query_params=(g.user['userID'], list_id,
                                                    bid_amt, bid_date))
            bid_id = cursor.lastrowid

            query = "UPDATE Listings SET bidID = %s WHERE listingID = %s;"
            db.execute_query(db_connection=db_conn, query=query,
                            query_params=(bid_id, list_id))

            flash(message, 'success')
            return redirect(url_for('root'))

@app.route('/submit-listing', methods=['POST'])
def submit_listing():
    if request.method == 'POST':
        data = request.get_json() 
        name = data.get('name')
        user_id = data.get('userID') 
        start_date = data['startDate']
        end_date = data['endDate']
        start_price = data['startPrice']
        buy_now_price = data.get('buyNowPrice', None)  
        description = data.get('description', None) 
        quantity = data['quantity']
        shipping_costs = data['shippingCosts']
        num_flagged = data['numFlagged']
        status = data['status']

        db_conn = db.connect_to_database()
        query = """
            INSERT INTO Listings (
                name, userID, startDate, endDate, startPrice, 
                buyNowPrice, description, quantity, shippingCosts, 
                numFlagged, status
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
        """
        db.execute_query(
            db_connection=db_conn, query=query,
            query_params=(
                name, user_id, start_date, end_date, start_price, 
                buy_now_price, description, quantity, shipping_costs, 
                num_flagged, status
            )
        )

        # Optionally, flash a success message and redirect
        # flash("Listing submitted successfully.", 'success')
        # return redirect(url_for('root'))

        return jsonify({"message": "Listing submitted successfully."}), 201

    # If not a POST request, you can handle it differently or raise an error
    return jsonify({"error": "Invalid request method."}), 405


# Listener
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 9112))
    app.run(port=port, debug=True)
