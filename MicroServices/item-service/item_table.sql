CREATE TABLE items (
                       item_id INT AUTO_INCREMENT PRIMARY KEY,
                       item_name VARCHAR(255),
                       owner_id INT,
                       description VARCHAR(1024),
                       category VARCHAR(255),
                       starting_bid DECIMAL(10,2),
                       buy_it_now_price DECIMAL(10,2),
                       warning BOOLEAN
);

CREATE TABLE watchlist (
                           user_id INT,
                           item_id INT,
                           PRIMARY KEY (user_id, item_id),
                           FOREIGN KEY (user_id) REFERENCES users(user_id),
                           FOREIGN KEY (item_id) REFERENCES items(item_id)
);

CREATE TABLE shopping_cart (
                               user_id INT,
                               item_id INT,
                               price DECIMAL(10, 2),
                               PRIMARY KEY (user_id, item_id),
                               FOREIGN KEY (user_id) REFERENCES users(user_id),
                               FOREIGN KEY (item_id) REFERENCES items(item_id)
);


