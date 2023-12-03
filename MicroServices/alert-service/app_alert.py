from flask import Flask, render_template, request, redirect, g, url_for, flash
import os
import database.db_connector as db
from flask_cors import CORS
# from datetime import date
from werkzeug.utils import secure_filename
from validation import validate_new_listing, validate_photo, validate_bid
import threading
# from datetime import datetime
import datetime
import time

# Set up upload folder
UPLOAD_FOLDER = 'static/img/'

# Initialize Flask app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config.from_mapping(SECRET_KEY='dev')
CORS(app)  # Enable CORS

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


# Listener
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 9112))
    app.run(port=port, debug=True)
