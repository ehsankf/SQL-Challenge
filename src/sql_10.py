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
                f"insert into {table_name} (user_id, created_at, liker_id) values (?, ?, ?)", 
                [
                    ('A', '2024-01-01 10:00:00', 'B'),
                    ('B', '2024-01-01 11:00:00', 'C'),
                    ('B', '2024-01-01 12:00:00', 'D'),
                    ('B', '2024-01-01 13:00:00', 'E'),
                    ('C', '2024-01-02 10:00:00', 'A'),
                    ('D', '2024-01-02 14:00:00', 'E'),
                    ('E', '2024-01-02 15:00:00', 'F'),
                    ('B', '2024-01-03 09:00:00', 'G'),
                    ('H', '2024-01-03 10:00:00', 'A'),
                    ('B', '2024-01-03 11:00:00', 'C'),
                    ('I', '2024-01-03 12:00:00', 'I')
                ]
            )
    conn.commit()
    

# Day 10
# Problem statement:
# A dating website’s schema is represented by a table 
# of people that like other people. The table has three columns. 
# One column is the user_id, another column is the liker_id which is the user_id 
# of the user doing the liking, and the last column is the date time that the like occurred.
# Write a query to count the number of liker’s likers (the users that like the likers) if the liker has one

table_name = "likes"
# delete table if exists
delete_table(conn, cursor, table_name)
# create tables
command = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        id INTEGER PRIMARY KEY,
        user_id VARCHAR(50),
        liker_id VARCHAR(50),
        created_at DATETIME
    )
"""
cursor.executescript(command)
conn.commit()

# add synthetic data
add_data()


command = f"""
select t1.user_id, count(distinct t2.liker_id) 
from {table_name} t1 
join {table_name} t2 on t1.liker_id=t2.user_id group by t1.user_id
"""
# cursor.executescript(command)  
rows = select_data(cursor, command)
for row in rows:
    print(row)

