from flask import Flask, jsonify, request
from pymongo import MongoClient
import bcrypt

app = Flask(__name__)

# MongoDB Connection
client = MongoClient('mongodb://localhost:27017/')
db = client.auction_system
users = db.users


@app.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')

    # Hashing
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    print(f"hashed_password: {hashed_password}")
    # Create user info
    user_record = {
        'username': username,
        'password': hashed_password,
        'is_suspended': False  # For admin suspend
    }

    users.insert_one(user_record)

    return jsonify({'message': 'Registered successfully!'}), 201

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password').encode('utf-8')  # 将用户输入的密码编码为字节串

    user_record = users.find_one({'username': username})

    if user_record and bcrypt.checkpw(password, user_record['password']):
        return jsonify({'message': 'Login successful!'}), 200
    else:
        return jsonify({'message': 'Invalid username or password'}), 401


if __name__ == '__main__':
    app.run(debug=True)
