import csv
import pymysql
from Database_Creation import create_database

# Connect to the MySQL database
conn = pymysql.connect(
    host='localhost',
    user='dbadmin',
    password='dbadmin',
    database='test123db'
)

# Create a cursor object using the cursor() method
cursor = conn.cursor()

# Open the CSV file
with open('menu_items_data.csv', newline='', encoding='utf-8') as csvfile:
    csv_reader = csv.reader(csvfile)
    next(csv_reader)  # Skip the header row
    for i,row in enumerate(csv_reader):
        # Prepare SQL query to insert data, excluding ItemID
        sql = '''INSERT INTO menuitems (ItemID, Name, Description, Price, Category)
                 VALUES (%s, %s, %s, %s, %s)'''
        # Extract values from the CSV row
        values = (i+1, row[1], row[2], float(row[3]), row[4])
        # Execute the SQL query
        cursor.execute(sql, values)

# Commit the transaction
conn.commit()

# Close the database connection
conn.close()

print('Data inserted successfully.')
