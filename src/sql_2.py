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
        f"insert into transactions (id, user_id, created_at, shipping_address) values (?, ?, ?, ?)", 
        [(1, 1, '2025-01-15 10:30:00', '123 Main St'),
        (2, 1, '2025-01-16 11:45:00', '789 Oak Ave'),
        (3, 2, '2025-01-17 14:20:00', '456 Elm St'),
        (4, 2, '2025-01-18 15:10:00', '123 Pine Rd'),
        (5, 3, '2025-01-19 16:05:00', '789 Oak Ave'),
        (6, 3, '2025-01-20 17:40:00', '123 Main St'),
        (7, 3, '2025-01-21 17:45:00', '123 Main St')]
    )
    conn.commit()

    cursor.executemany(
        f"insert into users (id, name, address) values (?, ?, ?)", 
        [(1, 'John Doe', '123 Main St'), 
         (2, 'Jane Smith', '456 Elm St'),
         (3, 'Alice Johnson', '789 Oak Ave')
        ]
    )
    conn.commit()
    

# Day 2
# Problem statement:
# Given a transactions table and a users table, write a query to determine whether users 
# tend to order more frequently to their primary (home) address compared to other addresses.
delete_table(conn, cursor, "users")
delete_table(conn, cursor, "transactions")
# create tables
command = """
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL, 
        created_at DATETIME,
        shipping_address VARCHAR(255)
    );
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        address TEXT

    )
"""
cursor.executescript(command)
conn.commit()

# add synthetic data
add_data()

# first approach
command = """
SELECT count(*), round(count(*)*1.0/nullif((select count(*) from transactions), 0), 2) as home_address_percent
from transactions t join users u on t.user_id=u.id
where t.shipping_address == u.address
"""

# second approach
command = """
SELECT round(sum(case when t.shipping_address == u.address then 1 else 0 end) * 1./count(*), 2.) as home_address_percent
from transactions t join users u on t.user_id=u.id;
"""

rows = select_data(cursor, command)
for row in rows:
    print(row)
