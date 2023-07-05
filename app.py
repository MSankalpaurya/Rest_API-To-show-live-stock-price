from flask import Flask, render_template, request, redirect, flash, session, jsonify
from flask_socketio import SocketIO, emit
import mysql.connector
from login.login import login_blueprint
from flask_jwt_extended import JWTManager, create_access_token
import threading

app = Flask(__name__)
app.secret_key = 'secret_key'
socketio = SocketIO(app)  # Initialize SocketIO

# Database connection details
host = 'localhost'
database = 'stock_db'
user = 'sankalp'
password = 'Jangoo@2022'

# Initialize JWTManager
jwt = JWTManager(app)

# Register the login routes
app.register_blueprint(login_blueprint)


# Function to fetch stock prices from the database
def get_stock_prices():
    db_connection = mysql.connector.connect(
        host=host,
        database=database,
        user=user,
        password=password
    )

    cursor = db_connection.cursor()

    cursor.execute("SELECT stock, price FROM stock_prices LIMIT 20")
    results = cursor.fetchall()

    stocks = [{'stock': stock, 'price': price} for stock, price in results]

    cursor.close()
    db_connection.close()

    return stocks

# Route for home page
@app.route("/home")
def home():
    return render_template('home.html')

# SocketIO event handler for initial stock prices
@socketio.on('connect')
def handle_connect():
    stocks = get_stock_prices()
    emit('stock_prices_update', stocks)

# Background thread to periodically update stock prices
def update_stock_prices():
    while True:
        stocks = get_stock_prices()
        socketio.emit('stock_prices_update', stocks)
        socketio.sleep(5)  # Update every 5 seconds

# Start the background thread when the application starts
socketio.start_background_task(update_stock_prices)

# # Homepage: Shows top 20 stocks and their current market price
# @app.route("/home")
# def home():
#     try:
#         # Connect to MySQL database
#         db_connection = mysql.connector.connect(
#             host=host,
#             database=database,
#             user=user,
#             password=password
#         )

#         cursor = db_connection.cursor()

#         # Retrieve top 20 stocks and their prices from the 'stock_prices' table
#         cursor.execute("SELECT stock, price FROM stock_prices LIMIT 20")
#         results = cursor.fetchall()

#         # Format the results as a list of dictionaries
#         stocks = [{'stock': stock, 'price': price} for stock, price in results]

#         cursor.close()
#         db_connection.close()

#         return render_template('home.html', stocks=stocks)
#     except mysql.connector.Error as error:
#         flash("Failed to connect to the database. Error: {}".format(error), "error")
#         return redirect("/")


# API endpoint to fetch updated stock prices
# @app.route("/api/stock_prices", methods=['GET'])
# def api_stock_prices():
#     try:
#         db_connection = mysql.connector.connect(
#             host=host,
#             database=database,
#             user=user,
#             password=password
#         )

#         cursor = db_connection.cursor()

#         # Retrieve top 20 stocks and their prices from the 'stock_prices' table
#         cursor.execute("SELECT stock, price FROM stock_prices LIMIT 20")
#         results = cursor.fetchall()

#         # Format the results as a list of dictionaries
#         stocks = [{'stock': stock, 'price': price} for stock, price in results]

#         cursor.close()
#         db_connection.close()

#         return jsonify(stocks)
#     except mysql.connector.Error as error:
        # return jsonify({'error': str(error)})


# Watchlist Page: Shows saved stocks
@app.route("/watchlist")
def watchlist():
    try:
        db_connection = mysql.connector.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )

        cursor = db_connection.cursor()

        # Retrieve saved stocks from the 'watchlist' table
        cursor.execute("SELECT stock, price FROM watchlist")
        results = cursor.fetchall()

        # Create a set to store unique stock names
        unique_stocks = set()

        # Format the results as a list of dictionaries and filter out duplicates
        stocks = []
        for stock, price in results:
            if stock not in unique_stocks:
                unique_stocks.add(stock)
                stocks.append({'stock': stock, 'price': price})

        cursor.close()
        db_connection.close()

        return render_template('watchlist.html', stocks=stocks)
    except mysql.connector.Error as error:
        flash("Failed to connect to the database. Error: {}".format(error), "error")
        return redirect("/")


# Save to Watchlist: Add stock to user's watchlist
@app.route("/save_to_watchlist", methods=['POST'])
def save_to_watchlist():
    stock = request.form['stock']
    price = request.form['price']

    try:
        db_connection = mysql.connector.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )

        cursor = db_connection.cursor()

        # Insert the stock into the 'watchlist' table
        query = "INSERT INTO watchlist (stock, price) VALUES (%s, %s)"
        values = (stock, price)
        cursor.execute(query, values)
        db_connection.commit()

        cursor.close()
        db_connection.close()

        flash("Stock saved to watchlist!", "success")
    except mysql.connector.Error as error:
        flash("Failed to save stock to watchlist. Error: {}".format(error), "error")

    return redirect("/home")


# Search Page: Allows users to search for stocks
@app.route("/search", methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_query = request.form['search_query']

        try:
            db_connection = mysql.connector.connect(
                host=host,
                database=database,
                user=user,
                password=password
            )

            cursor = db_connection.cursor()

            # Search for stocks based on the search query
            query = "SELECT stock, price FROM stock_prices WHERE stock LIKE %s"
            search_param = f"%{search_query}%"
            cursor.execute(query, (search_param,))
            results = cursor.fetchall()

            # Format the results as a list of dictionaries
            stocks = [{'stock': stock, 'price': price} for stock, price in results]

            cursor.close()
            db_connection.close()

            return render_template('search_results.html', search_query=search_query, stocks=stocks)
        except mysql.connector.Error as error:
            flash("Failed to connect to the database. Error: {}".format(error), "error")
            return redirect("/")

    return render_template('search.html')



if __name__ == "__main__":
    socketio.run(app, debug=True)
