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
                f"insert into {table_name} (id, user_id, job_id, posted_date) values (?, ?, ?, ?)", 
                [   (1, 1, 101, '2024-01-01'),
                    (2, 1, 102, '2024-01-02'),
                    (3, 2, 201, '2024-01-01'),
                    (4, 2, 201, '2024-01-15'),
                    (5, 2, 202, '2024-01-03'),
                    (6, 3, 301, '2024-01-01'),
                    (7, 4, 401, '2024-01-01'),
                    (8, 4, 401, '2024-01-15'),
                    (9, 4, 402, '2024-01-02'),
                    (10, 4, 402, '2024-01-16'),
                    (11, 5, 501, '2024-01-05'),
                    (12, 5, 502, '2024-01-10')]

            )
    conn.commit()
    

# Day 3
# Problem statement:
# Given a table of job postings, write a query to retrieve:

# The number of users who have posted each job only once
# The number of users who have posted at least one job multiple times
table_name = "job_postings"
delete_table(conn, cursor, table_name)
# create tables
command = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        job_id INTEGER NOT NULL,
        posted_date DATETIME NOT NULL
    )
"""
cursor.executescript(command)
conn.commit()

# add synthetic data
add_data()


command = """
with jobs as (
select user_id, job_id, count(*) as job_count from job_postings group by user_id, job_id
),
job_posting_counts_per_user as (
select user_id, max(job_count) as max_count from jobs group by user_id
)
select sum(case when max_count > 1 then 1 else 0 end) as multi_job_posting,  sum(case when max_count = 1 then 1 else 0 end) as single_job_posting from job_posting_counts_per_user
"""
# cursor.executescript(command)  
rows = select_data(cursor, command)
for row in rows:
    print(row)

