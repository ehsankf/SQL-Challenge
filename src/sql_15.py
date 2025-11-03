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
                f"insert into {table_name} ('id', 'credit_card', 'merchant', 'amount', 'transaction_time') values (?, ?, ?, ?, ?)", 
                [
                    (1, '1234-5678-9876', 'Amazon', 50.00, '2025-01-23 10:15:00'),
                    (2, '1234-5678-9876', 'Amazon', 50.00, '2025-01-23 10:20:00'),
                    (3, '6789-4321-1234', 'Walmart', 30.00, '2025-01-23 11:00:00'),
                    (4, '1234-5678-9876', 'Amazon', 50.00, '2025-01-23 10:30:00'),
                    (5, '6789-4321-1234', 'Walmart', 30.00, '2025-01-23 11:05:00'),
                    (6, '6789-4321-1234', 'BestBuy', 150.00, '2025-01-23 12:00:00'),
                    (7, '1234-5678-9876', 'Amazon', 50.00, '2025-01-23 12:10:00')
                ]
            )
    conn.commit()
    

# Day 15
# Problem statement:
# Using the transactions table, identify any payments made at the same merchant 
# with the same credit card for the same amount within 10 minutes of each other. 
# Count such repeated payments.
# Assumption:
# The first transaction of such payments should not be counted as a repeated payment. 
# This means that if a merchant performs 2 transactions with the same credit card and 
# for the same amount within 10 minutes, there will only be 1 repeated payment.

table_name = "transactions"
# delete table if exists
delete_table(conn, cursor, table_name)
# create tables
command = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        id INTEGER PRIMARY KEY,
        credit_card VARCHAR(50),
        merchant VARCHAR(50),
        amount DECIMAL(10, 2),
        transaction_time DATETIME
    )
"""
cursor.executescript(command)
conn.commit()

# add synthetic data
add_data()


command = f"""
select count(*)
from {table_name} t1 join {table_name} t2 
on t1.credit_card=t2.credit_card and t1.merchant=t2.merchant and t1.amount=t2.amount and 
t1.transaction_time < t2.transaction_time and t2.transaction_time <= datetime(t1.transaction_time, + '10 minutes')   
"""

# cursor.executescript(command)  
rows = select_data(cursor, command)
for row in rows:
    print(row)

