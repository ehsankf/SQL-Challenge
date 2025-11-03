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
                f"insert into {table_name} (id, transaction_value, created_at) values (?, ?, ?)", 
                [
                    (1, 50.00, '2025-01-23 10:15:00'),
                    (2, 30.00, '2025-01-23 15:45:00'),
                    (3, 20.00, '2025-01-23 18:30:00'),
                    (4, 45.00, '2025-01-24 09:20:00'),
                    (5, 60.00, '2025-01-24 22:10:00'),
                    (6, 25.00, '2025-01-25 11:30:00'),
                    (7, 35.00, '2025-01-25 14:50:00'),
                    (8, 55.00, '2025-01-25 19:05:00')
                ]
            )
    conn.commit()
    

# Day 4
# Problem statement:
# You’re given a table of customer sales in a retail store with the following columns:

# id: Transaction ID
# transaction_value: Monetary value of the transaction
# created_at: Timestamp of when the transaction occurred
# Write a query to retrieve the last transaction for each day.
# The output should include:

# The transaction ID
# The datetime of the transaction
# The transaction amount
# The results should be ordered chronologically by datetime.

table_name = "custome_sales"
# delete table if exists
delete_table(conn, cursor, table_name)
# create tables
command = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        id INTEGER PRIMARY KEY,
        transaction_value DECIMAL(10, 2) NOT NULL,
        created_at DATETIME NOT NULL
    )
"""
cursor.executescript(command)
conn.commit()

# add synthetic data
add_data()


command = f"""
with {table_name}_rank as (
    select id, created_at, transaction_value, row_number() over (partition by date(created_at) order by created_at desc) 
    as sale_rank from {table_name}
)
select id, created_at, transaction_value from {table_name}_rank where sale_rank=1 order by created_at asc
"""
# cursor.executescript(command)  
rows = select_data(cursor, command)
for row in rows:
    print(row)

