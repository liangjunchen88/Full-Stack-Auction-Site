# -*- coding:utf-8 -*-
# @Time : 2023/11/29 10:34
# @File : DetectExpiredListings.py

import sys
sys.path.append('../')

import schedule
import time
from datetime import datetime
import database.db_connector as db
from utils.EmailNotification import notify


# Connect to your MySQL database
db_conn = db.connect_to_database()

def check_expired_listings():
    now = datetime.now()

    query = "SELECT * FROM listings WHERE expirationDate <= %s"
    expired_listings = db.execute_query(
        db_connection=db_conn,
        query=query,
        query_params=(now,)
    ).fetchall()


    for listing in expired_listings:
        # TODO: Notify the winner by email (notification)
        # pseudocode: notify(listing['winner_email'])

        # TODO: add the item to the winner's shopping cart

        # TODO(optional): update some tables if necessary

        print(f"Expired listing: {listing}")

# Schedule the job to run every 5 seconds
schedule.every(5).seconds.do(check_expired_listings)

# Infinite loop to run the scheduler
while True:
    schedule.run_pending()
    time.sleep(1)
