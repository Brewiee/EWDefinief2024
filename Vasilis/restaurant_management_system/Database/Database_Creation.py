import pymysql


def create_database():
    DATABASE = input('Enter database name: ')
    # Connect to the MySQL database
    conn = pymysql.connect(
        host='localhost',
        user='dbadmin',
        password='dbadmin',
    )

    # Create a cursor object using the cursor() method
    cursor = conn.cursor()

    # Create the database testdb
    cursor.execute('CREATE DATABASE IF NOT EXISTS %s' % DATABASE)
    database = DATABASE
    return database

def create_tables():
    DATABASE = create_database()
    conn = pymysql.connect(
        host='localhost',
        user='dbadmin',
        password='dbadmin',
        database=DATABASE
    )


    # Create a cursor object using the cursor() method
    cursor = conn.cursor()

    # Create tables
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS menuitems (
        ItemID INT PRIMARY KEY,
        Name VARCHAR(255),
        Description TEXT,
        Price DECIMAL(10,2),
        Category VARCHAR(255)
    )''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tables (
        TableID INT PRIMARY KEY,
        Number INT,
        Seats INT,
        Status ENUM('available', 'occupied', 'reserved')
    )''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        OrderID INT PRIMARY KEY,
        UserID INT,
        TableNumber INT,
        OrderTime DATETIME,
        Status ENUM('placed', 'prepared', 'served', 'paid'),
        FOREIGN KEY (UserID) REFERENCES users(UserID),
        FOREIGN KEY (TableNumber) REFERENCES tables(TableID)
    )''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS orderdetails (
        OrderDetailID INT PRIMARY KEY,
        OrderID INT,
        ItemID INT,
        Quantity INT,
        Subtotal DECIMAL(10,2),
        FOREIGN KEY (OrderID) REFERENCES orders(OrderID),
        FOREIGN KEY (ItemID) REFERENCES menuitems(ItemID)
    )''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS customer (
        customer_id INT PRIMARY KEY,
        name VARCHAR(100),
        address VARCHAR(255),
        email VARCHAR(100),
        phone_number VARCHAR(20)
    )''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS reservation (
        reservation_id INT PRIMARY KEY,
        customer_id INT,
        reservation_date DATE,
        reservation_time TIME,
        party_size INT,
        TableID INT,
        FOREIGN KEY (customer_id) REFERENCES customer(customer_id),
        FOREIGN KEY (TableID) REFERENCES tables(TableID)
    )''')

    # Commit the transaction
    conn.commit()

    # Close the database connection
    conn.close()

    print('Database and tables created successfully.')

create_tables()
