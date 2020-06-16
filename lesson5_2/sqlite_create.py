import sqlite3

connection = sqlite3.connect('business.db')
connection.execute('CREATE TABLE products (prodname, price, weight)')
connection.execute('CREATE TABLE users (name, password, email)')
connection.execute('CREATE TABLE apartments (name, rent, rooms)')