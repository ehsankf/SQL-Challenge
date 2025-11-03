import sqlite3

import random 
from datetime import datetime, timedelta 

from utils import *

# Connect to (or create) a database file
conn = sqlite3.connect("sql_challenge.db")

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

def add_data():
    
    cursor.executemany(
                f"insert into {table_name1} (product_id, price) values (?, ?)", 
                [
                    (1, 100.00),
                    (2, 150.00),
                    (3, 75.00),
                    (4, 200.00),
                    (5, 120.00)
                ]
            )
    conn.commit()

    cursor.executemany(
                f"insert into {table_name2} (transaction_id, product_id, amount) values (?, ?, ?)", 
                [
                    (1, 1, 95.00),
                    (2, 1, 98.00),
                    (3, 2, 145.00),
                    (4, 2, 150.00),
                    (5, 3, 70.00),
                    (6, 4, 190.00),
                    (7, 4, 195.00),
                    (8, 5, 115.00)
                ]
            )
    conn.commit()

# Day 6
# Problem statement:
# Given two tables — transactions and products — write a query to return the:
# product_id
# product_price
# average transaction price
# for all products where the product price is greater than the average transaction price.

table_name1 = "products"
table_name2 = "transactions"

# delete table if exists
delete_table(conn, cursor, table_name1)
delete_table(conn, cursor, table_name2)
# create tables
command = f"""
    CREATE TABLE IF NOT EXISTS {table_name1} (
        product_id INTEGER PRIMARY KEY,
        price DECIMAL(10, 2) NOT NULL
    );
    CREATE TABLE IF NOT EXISTS {table_name2} (
        transaction_id INTEGER PRIMARY KEY,
        product_id INTEGER,
        amount DECIMAL(10, 2) NOT NULL,
        FOREIGN KEY (product_id) REFERENCES {table_name1}(product_id)
    );
"""
cursor.executescript(command)
conn.commit()

# # add synthetic data
add_data()


command = f"""
with {table_name2}_average as 
(
    select avg(amount) as trans_avg from {table_name2}
)
select product_id, price, t.trans_avg from {table_name1} cross join {table_name2}_average t where price > t.trans_avg
"""

# cursor.executescript(command)  
rows = select_data(cursor, command)
for row in rows:
    print(row)

