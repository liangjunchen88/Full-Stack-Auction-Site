from flask import Flask, jsonify, request

app = Flask(__name__)

# Temporary data store. In a real application, you would use a database.
reviews = []

@app.route('/reviews', methods=['GET'])
def get_reviews():
    return jsonify(reviews)

@app.route('/reviews', methods=['POST'])
def submit_review():
    review_data = request.json
    reviews.append(review_data)
    return jsonify({"message": "Review submitted successfully"}), 201

# Start the Flask application
if __name__ == '__main__':
    app.run(debug=True)
