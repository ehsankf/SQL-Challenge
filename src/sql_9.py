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
                f"insert into {table_name} (month, product_id, amount_sold) values (?, ?, ?)", 
                [
                    ('2021-01-01', 1, 100),
                    ('2021-01-01', 2, 50),
                    ('2021-01-01', 3, 150),
                    ('2021-02-01', 1, 50),
                    ('2021-02-01', 2, 250),
                    ('2021-03-01', 1, 120),
                    ('2021-03-01', 2, 350),
                    ('2021-03-01', 3, 200),
                    ('2021-04-01', 1, 200),
                    ('2021-05-01', 3, 175),
                    ('2021-06-01', 1, 0),
                    ('2021-06-01', 2, 100),
                    ('2021-06-01', 4, 250)
                ]
            )
    conn.commit()
    

# Day 9
# Problem statement:
# Given a table containing data for monthly sales, 
# write a query to find the total amount of each product 
# sold for each month, with each product as its own column in the output table.

table_name = "custome_sales"
# delete table if exists
delete_table(conn, cursor, table_name)
# create tables
command = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        month DATE,
        product_id INTEGER,
        amount_sold INTEGER
    )
"""
cursor.executescript(command)
conn.commit()

# add synthetic data
add_data()


command = f"""
select 
month,
sum(case when product_id=1 then amount_sold else 0 end) as product_1, 
sum(case when product_id=2 then amount_sold else 0 end) as product_2, 
sum(case when product_id=3 then amount_sold else 0 end) as product_3, 
sum(case when product_id=4 then amount_sold else 0 end) as product_4 
from {table_name} group by month
"""
# cursor.executescript(command)  
rows = select_data(cursor, command)
for row in rows:
    print(row)

