from flask import Flask, jsonify, request
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/auction_db'
mongo = PyMongo(app)

# Sample data to simulate an auction item
auction_item = {
    'id': 'SampleId',
    'starting_price': None,
    'current_bid': None,
    'bidder': None,
    'bidding_items': None,
    'is_buynow': False,
    'start_time': None,
    'auction_window': None,
    'auction_started': False,
    'auction_ended': False
}


@app.route('/startAuction', methods=['POST'])
def start_auction():
    global auction_item

    if not auction_item['auction_started']:
        data = request.get_json()

        if 'items' in data and 'start_time' in data and 'auction_window' in data and 'starting_price' in data:
            items = data['items']
            start_time = data['start_time']
            auction_window = data['auction_window']
            starting_price = data['starting_price']

            # Update auction data
            auction_item['bidding_items'] = items
            auction_item['starting_price'] = starting_price
            auction_item['current_bid'] = auction_item['starting_price']
            auction_item['bidder'] = None
            auction_item['start_time'] = start_time
            auction_item['auction_window'] = auction_window

            auction_item['auction_started'] = False
            auction_item['auction_ended'] = False

            # Update MongoDB document
            mongo.db.auction_item.update({}, {"$set": {
                'id': 'SampleId',
                'starting_price': starting_price,
                'current_bid': starting_price,
                'bidder': None,
                'bidding_items': items,
                'is_buynow': False,
                'start_time': None,
                'auction_window': auction_window,
                'auction_started': False,
                'auction_ended': False
            }})

            return jsonify({'message': 'Auction started successfully'}), 200
        else:
            return jsonify({'message': 'Missing required parameters'}), 400
    else:
        return jsonify({'message': 'Auction is already in progress'}), 400


@app.route('/placeBid', methods=['POST'])
def place_bid():
    global auction_item

    if auction_item['auction_started'] and not auction_item['auction_ended']:
        data = request.get_json()

        if 'bid_amount' in data:
            bid_amount = float(data['bid_amount'])

            if bid_amount > auction_item['current_bid']:
                auction_item['current_bid'] = bid_amount
                auction_item['bidder'] = data.get('bidder', 'Anonymous')

                # Update MongoDB document
                mongo.db.auction_item.update(
                    {}, {"$set": {'current_bid': bid_amount, 'bidder': auction_item['bidder']}})

                return jsonify({'message': 'Bid placed successfully'}), 200
            else:
                return jsonify({'message': 'Bid must be higher than the current bid'}), 400
        else:
            return jsonify({'message': 'Bid amount not provided'}), 400
    else:
        return jsonify({'message': 'Auction has not started or has already ended'}), 400


if __name__ == '__main__':
    app.run(debug=True)
