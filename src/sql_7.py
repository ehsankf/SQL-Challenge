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
                f"insert into {table_name} ('id', 'user_id', 'created_at', 'product_id', 'quantity') values (?, ?, ?, ?, ?)", 
                [
                    (1, 101, '2024-01-01 10:00:00', 1, 3),
                    (2, 101, '2024-01-01 11:00:00', 2, 3),
                    (3, 102, '2024-01-02 09:00:00', 1, 2),
                    (4, 102, '2024-01-02 11:00:00', 2, 3),
                    (5, 102, '2024-01-02 15:00:00', 3, 1),
                    (6, 103, '2024-01-02 10:00:00', 1, 3),
                    (7, 104, '2024-01-01 09:00:00', 2, 3),
                    (8, 104, '2024-01-02 10:00:00', 3, 2),
                    (9, 104, '2024-01-03 11:00:00', 4, 1),
                    (10, 101, '2024-01-15 11:00:00', 3, 1),
                ]
            )
    conn.commit()
    

# Day 7
# Problem statement:
# We’re given a table containing user product purchases, where each row represents a unique purchase by a user.
# Write a query to calculate the number of customers that were upsold by purchasing additional products.

# Note: If a customer purchases multiple products on the same day, it does not count as an upsell. 
# Upsell is recognized only when purchases occur on separate days.

table_name = "transactions"
# delete table if exists
delete_table(conn, cursor, table_name)
# create tables
command = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        product_id INTEGER,
        quantity INTEGER,
        created_at DATETIME
    )
"""
cursor.executescript(command)
conn.commit()

# add synthetic data
add_data()


command = f"""
select count(*) as upsold_customer_count from (
select user_id
from {table_name} group by user_id having(count(distinct date(created_at))>1))
"""
# cursor.executescript(command)  
rows = select_data(cursor, command)
for row in rows:
    print(row)

