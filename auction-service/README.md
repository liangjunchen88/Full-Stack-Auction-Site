# Auction API

This Flask-based API provides main endpoints for managing auctions.

## 1. Start Auction

- Endpoint:

  - **URL:** `/startAuction`
  - **Method:** `POST`

- Description:

  Initiates a new auction for a specific item with user-defined parameters.

- Request Body:

  ```json
  {
    "bidding_items": "Chocolate",
    "starting_price": 50.0,
    "start_time": "YYYY-MM-DD HH:MM:SS",
    "auction_window": "HH:MM:SS"
  }
  ```

  - **bidding_items:** items to be auctioned.
  - **start_time:** Date and time when the auction should start (in the format "YYYY-MM-DD HH:MM:SS").
  - **auction_window:** Duration of the auction window (in the format "HH:MM:SS").

- Response:
  - **200 OK:** Auction started successfully.
  - **400 Bad Request:** Missing required parameters or auction

### 2. Place Bid

- **Endpoint:**
  - URL: `/placeBid`
  - Method: `POST`

- **Description:**
  - Allows users to place bids on an ongoing auction.

- **Request Body:**

    ```json
    {
      "bid_amount": 75.0,
      "bidder": "Andy"
    }
    ```

    - **bid_amount:** Amount the user wants to bid on the item.
    - **bidder:** Name of the bidder.

- **Response:**
  - **200 OK:** Bid placed successfully.
  - **400 Bad Request:** Bid amount not provided, bid must be higher than the current bid, or auction has not started or has already ended.
