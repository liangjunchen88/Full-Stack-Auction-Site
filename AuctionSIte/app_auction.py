from flask import Flask, render_template, request, redirect, g, url_for, flash
import os
import database.db_connector as db
# from datetime import date
from werkzeug.utils import secure_filename
import auth
from validation import validate_new_listing, validate_photo, validate_bid
import threading
# from datetime import datetime
import datetime
import database.db_connector as db


UPLOAD_FOLDER = 'static/img/'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config.from_mapping(SECRET_KEY='dev')
app.register_blueprint(auth.bp)


# The function for keep looping and check the status of the listings
def update_listing_status():
    while True:
        current_time = datetime.now()
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


@app.route('/submit-listing', methods=['GET', 'POST'])
@auth.login_required
def submit_listing():

    db_conn = db.connect_to_database()

    if request.method == "GET":
        return render_template('submit_listing.j2')

    if request.method == 'POST':
        data = request.form
        error = validate_new_listing(data)

        if error:
            flash(error, 'danger')
            return render_template('submit_listing.j2')

        # validated, parse form and add listing
        name = data['name']
        startPrice = data['startPrice']
        description = data['description']
        quantity = data['quantity']
        shippingCosts = data['shippingCosts']

        list_date = date.today()
        expiration = data['expiration']

        # user photo stored at static/img/ otherwise default photo used
        photo = request.files['photo']
        filepath = "./static/img/No_image_available.jpg"
        if validate_photo(photo):
            filename = secure_filename(photo.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            photo.save(filepath)

        query = "INSERT INTO Listings (name, userID, listDate, expirationDate, startPrice, description, quantity, shippingCosts) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"
        cursor = db.execute_query(
            db_connection=db_conn, query=query, query_params=(name, g.user['userID'], list_date, expiration, startPrice, description, quantity, shippingCosts))
        list_id = cursor.lastrowid

        query = "INSERT INTO Photos (photoPath, listingID) VALUES (%s, %s);"
        db.execute_query(db_connection=db_conn, query=query,
                         query_params=(filepath, list_id))

        return redirect(url_for('root'))


# Listener
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 9112))
    app.run(port=port, debug=True)
