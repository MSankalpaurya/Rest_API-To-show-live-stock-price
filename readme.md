# Stock App

The Stock App is a web application built with Flask that displays and updates stock prices in real-time. It provides features such as viewing stock prices, saving stocks to a watchlist, and searching for stocks.

## Installation

1. Clone the repository:

>> Where uploaded


2. Change into the project directory:

cd stock-app

## Set-up mysql-databse

1. give permission to the script file to execute it : 

chmod +x script.sh

2. Execute it:

./script.sh

## Log-in details

Username: abc
Password: 1234

3. Install the required dependencies:

pip install -r requirements.txt

## Usage

1. Run the `create_stock_db.py` script in a separate terminal to initialize and update the stock prices database:

python create_stock_db.py


2. Start the Flask development server:

python app.py

3. Access the application in your web browser at `http://localhost:5000`.

## Known Bugs

- There are no known bugs but future prospect of improvement.

## Future Prospects

- Implement user registration and authentication functionality for personalized watchlists.
- Logic for login/regsistration is a work in progress
- Need to implement JWT for login
- Need logic to fetch data from any live database, once permission is granted
- Enhance the search functionality by integrating with external APIs to provide additional stock information.
- In watchlist tab, option to modify, make favourites etc
- Improve the user interface and design of the application.
- Optimize the database queries and update mechanism for better performance.


