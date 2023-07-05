import random
import mysql.connector
import time

# Database connection details
host = 'localhost'
database = 'stock_db'
user = 'sankalp'
password = 'Jangoo@2022'

# Connect to MySQL server
db_connection = mysql.connector.connect(
    host=host,
    database=database,
    user=user,
    password=password
)

# Create a cursor to interact with the server
cursor = db_connection.cursor()

# Switch to the 'stock_db' database
cursor.execute("USE stock_db")

# Delete all records from the 'stock_prices' table
cursor.execute("DELETE FROM stock_prices")

# List of stock names to keep
stock_names = [
    'Reliance Industries Limited',
    'Tata Consultancy Services Limited',
    'HDFC Bank Limited',
    'Infosys Limited',
    'Housing Development Finance Corporation Limited',
    'ICICI Bank Limited',
    'Kotak Mahindra Bank Limited',
    'Hindustan Unilever Limited',
    'State Bank of India',
    'ITC Limited',
    'Larsen & Toubro Limited',
    'Maruti Suzuki India Limited',
    'Asian Paints Limited',
    'Axis Bank Limited',
    'Bajaj Finance Limited',
    'Mahindra & Mahindra Limited',
    'Wipro Limited',
    'HCL Technologies Limited',
    'Bajaj Auto Limited',
    'Tech Mahindra Limited',
    'UltraTech Cement Limited',
    'Nestle India Limited',
    'Dr. Reddy\'s Laboratories Limited',
    'Power Grid Corporation of India Limited',
    'Adani Ports and Special Economic Zone Limited',
    'Tata Motors Limited',
    'Coal India Limited',
    'Sun Pharmaceutical Industries Limited',
    'Hero MotoCorp Limited',
    'IndusInd Bank Limited'
]

# Generate random prices for each stock name
stock_prices = {stock: round(random.uniform(100, 500), 2) for stock in stock_names}

# Insert stock prices into the 'stock_prices' table
for stock, price in stock_prices.items():
    sql = "INSERT INTO stock_prices (stock, price) VALUES (%s, %s)"
    values = (stock, price)
    cursor.execute(sql, values)

# Commit the changes to the database
db_connection.commit()

print("Initial stock values saved to the database.")

try:
    while True:
        # Update stock prices every 10 seconds
        time.sleep(0.02)

        # Generate new random prices for each stock
        stock_prices = {stock: round(random.uniform(100, 500), 2) for stock in stock_names}

        for stock, price in stock_prices.items():
            sql = "UPDATE stock_prices SET price = %s WHERE stock = %s"
            values = (price, stock)
            cursor.execute(sql, values)

        # Commit the changes to the database
        db_connection.commit()

        print("Stock values updated.")
except KeyboardInterrupt:
    print("\nStock value update stopped by user.")

# Close the cursor and database connection
cursor.close()
db_connection.close()
