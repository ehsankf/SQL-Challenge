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
                f"insert into {table_name1} ('id', 'price') values (?, ?)", 
                [
                    (101, 20.00),
                    (102, 15.00),
                    (103, 30.00)
                ]
            )
    cursor.executemany(
                f"insert into {table_name2} ('id', 'product_id', 'quantity', 'created_at') values (?, ?, ?, ?)", 
                [
                    (1, 101, 2, '2019-01-15 10:00:00'),
                    (2, 102, 1, '2019-01-20 12:00:00'),
                    (3, 101, 3, '2019-02-10 14:00:00'),
                    (4, 103, 1, '2019-02-25 10:15:00'),
                    (5, 102, 4, '2019-03-05 09:30:00'),
                    (6, 101, 1, '2019-03-18 11:45:00')
                ]
            )
    conn.commit()
    

# Day 14
# Problem statement:
# Given a table of transactions and products, write a function to get the 
# month_over_month change in revenue for the year 2019. Make sure to round 
# month_over_month to 2 decimal places.

table_name1 = "products"
table_name2 = "transactions"

# delete table if exists
delete_table(conn, cursor, table_name1)
delete_table(conn, cursor, table_name2)
# create tables
command = f"""
    CREATE TABLE IF NOT EXISTS {table_name1} (
        id INTEGER PRIMARY KEY,
        price DECIMAL(10, 2)
    );
    CREATE TABLE IF NOT EXISTS {table_name2} (
        id INTEGER PRIMARY KEY,
        product_id INTEGER,
        quantity INTEGER,
        created_at TIMESTAMP,
        FOREIGN KEY (product_id) REFERENCES {table_name1}(id)
    );
"""
cursor.executescript(command)
conn.commit()

# add synthetic data
add_data()


command = f"""
with {table_name1}_per_mounth_revenue as 
(
    select cast(strftime('%m', created_at) as integer) created_at_month, sum(price*quantity) revenue from {table_name1} t1 join {table_name2} t2 on t2.product_id=t1.id
where created_at between '2019-01-01' and '2019-12-31' group by created_at_month
),
{table_name1}_prev_mounth_revenue as 
(
   select created_at_month, revenue, lag(revenue) over (order by created_at_month) prev_mounth_revenue 
from {table_name1}_per_mounth_revenue 
)
select created_at_month, round(100.*(revenue - prev_mounth_revenue)*1./nullif(prev_mounth_revenue, 0), 2) from {table_name1}_prev_mounth_revenue
"""
# select * from {table_name1}_per_mounth_by_mounth_revenue where month_over_month_rev is not null

# cursor.executescript(command)  
rows = select_data(cursor, command)
for row in rows:
    print(row)

