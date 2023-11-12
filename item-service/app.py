from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

def create_connection():
    """Create a database connection."""
    connection = None
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='username',
            password='password',
            database='database'
        )
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection

@app.route('/add_shopping_cart', methods=['POST'])
def add_shopping_cart():
    """Add item to shopping cart."""
    data = request.json
    connection = create_connection()
    cursor = connection.cursor()

    user_id = data['user_id']
    item_id = data['item_id']
    price = data['price']

    query = "INSERT INTO shopping_cart (user_id, item_id, price) VALUES (%s, %s, %s)"
    cursor.execute(query, (user_id, item_id, price))
    connection.commit()

    return jsonify({"message": "Item added to shopping cart"}), 201

@app.route('/add_watchlist', methods=['POST'])
def add_watchlist():
    """Add item to watchlist."""
    data = request.json
    connection = create_connection()
    cursor = connection.cursor()

    user_id = data['user_id']
    item_id = data['item_id']

    query = "INSERT INTO watchlist (user_id, item_id) VALUES (%s, %s)"
    cursor.execute(query, (user_id, item_id))
    connection.commit()

    return jsonify({"message": "Item added to watchlist"}), 201

if __name__ == '__main__':
    app.run(debug=True)