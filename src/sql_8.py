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
                f"insert into {table_name} (id, title, start_date, end_date, budget) values (?, ?, ?, ?, ?)", 
                [
                    (1, 'Website Redesign', '2024-01-01', '2024-02-15', 50000),
                    (2, 'Mobile App Dev', '2024-02-15', '2024-04-01', 75000),
                    (3, 'Database Migration', '2024-04-01', '2024-05-15', 60000),
                    (4, 'Cloud Integration', '2024-03-01', '2024-04-15', 45000),
                    (5, 'Security Audit', '2024-05-15', '2024-06-30', 30000)
                ]
            )
    conn.commit()
    

# Day 8
# Problem statement:
# Write a query to return pairs of projects where the end date 
# of one project matches the start date of another project.

table_name = "projects"
# delete table if exists
delete_table(conn, cursor, table_name)
# create tables
command = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        id INTEGER PRIMARY KEY,
        title VARCHAR(100),
        start_date DATETIME,
        end_date DATETIME,
        budget DECIMAL(10, 2)
    )
"""
cursor.executescript(command)
conn.commit()

# add synthetic data
add_data()


command = f"""
select t1.title p_title_end, t2.title p_title_start, t1.end_date p_date from {table_name} t1 join {table_name} t2
on t1.end_date=t2.start_date
"""
# cursor.executescript(command)  
rows = select_data(cursor, command)
for row in rows:
    print(row)

