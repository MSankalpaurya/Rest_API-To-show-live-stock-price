#!/bin/bash

# Install MySQL Server
sudo apt update
sudo apt install mysql-server -y

# Start MySQL service
sudo systemctl start mysql

# Enable MySQL service to start on boot
sudo systemctl enable mysql

# Create database
mysql -u root -e "CREATE DATABASE stock_db;"

# Create user and grant privileges
mysql -u root -e "CREATE USER 'Sankalp'@'localhost' IDENTIFIED BY 'Jangoo@2022';"
mysql -u root -e "GRANT ALL PRIVILEGES ON stock_db.* TO 'Sankalp'@'localhost';"
mysql -u root -e "FLUSH PRIVILEGES;"

# Connect to the database
mysql -u Sankalp -pJangoo@2022 -e "USE stock_db;"

# Create 'stock_prices' table
mysql -u Sankalp -pJangoo@2022 -e "CREATE TABLE stock_prices (stock VARCHAR(255), price FLOAT);"

# Create 'watchlist' table
mysql -u Sankalp -pJangoo@2022 -e "CREATE TABLE watchlist (stock VARCHAR(255), price FLOAT);"

echo "MySQL setup completed successfully!"
