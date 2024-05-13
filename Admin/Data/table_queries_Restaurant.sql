CREATE TABLE IF NOT EXISTS menuitems (
    ItemID INT PRIMARY KEY,
    Name VARCHAR(255),
    Description TEXT,
    Price DECIMAL(10,2),
    Category VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS users (
    UserID INT PRIMARY KEY,
    Username VARCHAR(255),
    Password VARCHAR(255),
    Role ENUM('admin', 'staff'),
    FullName VARCHAR(255),
    ContactInfo VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS tables (
    TableID INT PRIMARY KEY,
    Number INT,
    Seats INT,
    Status ENUM('available', 'occupied', 'reserved')
);

CREATE TABLE IF NOT EXISTS orders (
    OrderID INT PRIMARY KEY,
    UserID INT,
    TableNumber INT,
    OrderTime DATETIME,
    Status ENUM('placed', 'prepared', 'served', 'paid'),
    FOREIGN KEY (UserID) REFERENCES users(UserID),
    FOREIGN KEY (TableNumber) REFERENCES tables(TableID)
);

CREATE TABLE IF NOT EXISTS orderdetails (
    OrderDetailID INT PRIMARY KEY,
    OrderID INT,
    ItemID INT,
    Quantity INT,
    Subtotal DECIMAL(10,2),
    FOREIGN KEY (OrderID) REFERENCES orders(OrderID),
    FOREIGN KEY (ItemID) REFERENCES menuitems(ItemID)
);

CREATE TABLE IF NOT EXISTS customer (
    customer_id INT PRIMARY KEY,
    name VARCHAR(100),
    address VARCHAR(255),
    email VARCHAR(100),
    phone_number VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS reservation (
    reservation_id INT PRIMARY KEY,
    customer_id INT,
    reservation_date DATE,
    reservation_time TIME,
    party_size INT,
    TableID INT,
    FOREIGN KEY (customer_id) REFERENCES customer(customer_id),
    FOREIGN KEY (TableID) REFERENCES tables(TableID)
);