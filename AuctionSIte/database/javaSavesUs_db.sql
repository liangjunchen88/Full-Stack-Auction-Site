DROP TABLE IF EXISTS Users;

CREATE TABLE Users (
    userID INT(11) UNIQUE NOT NULL AUTO_INCREMENT,
    userName VARCHAR(255) UNIQUE NOT NULL ,
    password VARCHAR(255) NOT NULL,
    firstName VARCHAR(255) NOT NULL,
    lastName VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    dateJoined DATE NOT NULL,
    PRIMARY KEY (userID)
);

INSERT INTO Users (userName, password, firstName, lastName, email, dateJoined) VALUES
                                                                                   ('johndoe', 'pbkdf2:sha256:150000$iD5kR8qS$01a43a001a115b0747ed312a66686405225c1658ab8bf57f5a46e94d0393039e', 'John', 'Doe', 'johndoe@gmail.com', '2024-04-04');

DROP TABLE IF EXISTS Listings;

CREATE TABLE Listings (
    listingID INT(11) UNIQUE NOT NULL AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    userID INT(11),
    bidID INT(11),
    discription VARCHAR(255) NOT NULL,
    listDate DATE NOT NULL,
    expirationDate DATE NOT NULL,
    PRIMARY KEY (listingID),
    FOREIGN KEY (userID) REFERENCES Users(userID)
);

INSERT INTO Listings (name, userID, bidID, listDate, expirationDate) VALUES
    ('dummy item',1, NULL, '2020-04-04', '2022-06-06');
DROP TABLE IF EXISTS Bids;

CREATE TABLE Bids (
    bidID INT(11) UNIQUE NOT NULL AUTO_INCREMENT,
    userID INT(11) NOT NULL,
    listingID INT(11) NOT NULL,
    bidAmt INT(11) NOT NULL,
    bidDate DATE NOT NULL,
    PRIMARY KEY (bidID),
    FOREIGN KEY (userID) REFERENCES Users(userID),
    FOREIGN KEY (listingID) REFERENCES Listings(listingID)
);

ALTER TABLE Listings
ADD FOREIGN KEY (bidID) REFERENCES Bids(bidID);

INSERT INTO Bids (userID, listingID, bidAmt, bidDate) VALUES 
    (1, 1, 20000, '2023-11-15');

UPDATE Listings SET bidID = 1 WHERE listingID = 1;

DROP TABLE IF EXISTS Features;



DROP TABLE IF EXISTS Photos;

CREATE TABLE Photos (
    photoID INT(11) UNIQUE NOT NULL AUTO_INCREMENT,
    listingID INT(11) NOT NULL,
    photoPath VARCHAR(255) NOT NULL,
    PRIMARY KEY (photoID),
    FOREIGN KEY (listingID) REFERENCES Listings(listingID)
);

INSERT INTO Photos (listingID, photoPath) VALUES
    (1, 'static/img/65-mustang.jpg');

