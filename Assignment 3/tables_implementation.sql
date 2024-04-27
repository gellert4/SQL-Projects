use book_store;

-- Create Books Table
CREATE TABLE IF NOT EXISTS Books (
    isbn CHAR(10) PRIMARY KEY,
    author VARCHAR(100) NOT NULL,
    title VARCHAR(200) NOT NULL,
    price FLOAT NOT NULL,
    subject VARCHAR(100) NOT NULL
);

-- Create Members Table
CREATE TABLE IF NOT EXISTS Members (
    userid INT PRIMARY KEY,
    fname VARCHAR(50) NOT NULL,
    lname VARCHAR(50) NOT NULL,
    address VARCHAR(50) NOT NULL,
    city VARCHAR(30) NOT NULL,
    zip INT NOT NULL,
    phone VARCHAR(15),
    email VARCHAR(40) NOT NULL UNIQUE,
    password VARCHAR(200) NOT NULL
);

-- Create Orders Table
CREATE TABLE IF NOT EXISTS Orders (
    userid INT,
    ono INT PRIMARY KEY,
    create_date DATE,
    shipAddress VARCHAR(50),
    shipCity VARCHAR(30),
    shipZip INT,
    FOREIGN KEY (userid) REFERENCES Members(userid)
);

-- Create OrderDetails Table
CREATE TABLE IF NOT EXISTS OrderDetails (
    ono INT,
    isbn CHAR(10),
    qty INT NOT NULL,
    amount FLOAT NOT NULL,
    PRIMARY KEY (ono, isbn),
    FOREIGN KEY (ono) REFERENCES Orders(ono),
    FOREIGN KEY (isbn) REFERENCES Books(isbn)
);

-- Create Cart Table
CREATE TABLE IF NOT EXISTS Cart (
    userid INT,
    isbn CHAR(10),
    qty INT NOT NULL,
    PRIMARY KEY (userid, isbn),
    FOREIGN KEY (userid) REFERENCES Members(userid),
    FOREIGN KEY (isbn) REFERENCES Books(isbn)
);

-- Create Relationships
ALTER TABLE OrderDetails ADD CONSTRAINT fk_odetails_books FOREIGN KEY (isbn) REFERENCES Books(isbn);
ALTER TABLE Orders ADD CONSTRAINT fk_orders_members FOREIGN KEY (userid) REFERENCES Members(userid);
