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
                f"insert into {table_name} ('user_id', 'created_at', 'url') values (?, ?, ?)", 
                [
                    (1, '2019-12-30 10:00:00', 'https://example.com/2019-page1'),
                    (1, '2019-12-31 11:00:00', 'https://example.com/2019-page2'),
                    (2, '2019-11-15 12:00:00', 'https://example.com/2019-profile12'),
                    (3, '2019-11-16 13:00:00', 'https://example.com/2019-profile62'),
                    (4, '2019-10-20 14:00:00', 'https://example.com/2019-blog1'),
                    (4, '2019-09-29 10:00:00', 'https://example.com/2019-review'),
                    (5, '2019-08-28 15:00:00', 'https://example.com/2019-survey'),
                    (6, '2019-08-30 18:00:00', 'https://example.com/2019-summer1'),
                    (6, '2019-08-31 19:00:00', 'https://example.com/2019-summer2'),
                    (1, '2019-09-15 20:00:00', 'https://example.com/2019-page1'),
                    (1, '2019-09-15 21:00:00', 'https://example.com/2019-page2'),
                    (1, '2020-01-01 10:00:00', 'https://example.com/page1'),
                    (1, '2020-01-02 11:00:00', 'https://example.com/page2'),
                    (1, '2020-01-04 12:00:00', 'https://example.com/page3'),
                    (1, '2020-01-05 13:00:00', 'https://example.com/page4'),
                    (1, '2020-01-06 14:00:00', 'https://example.com/page5'),
                    (1, '2020-01-07 12:00:00', 'https://example.com/page7'),
                    (1, '2020-01-08 10:00:00', 'https://example.com/page8'),
                    (1, '2020-01-09 12:00:00', 'https://example.com/page9'),
                    (1, '2020-01-10 12:00:00', 'https://example.com/page10'),
                    (2, '2020-02-10 15:00:00', 'https://example.com/dashboard'),
                    (2, '2020-02-11 16:00:00', 'https://example.com/profile'),
                    (2, '2020-02-13 17:00:00', 'https://example.com/settings'),
                    (2, '2020-02-14 18:00:00', 'https://example.com/messages'),
                    (2, '2020-02-15 19:00:00', 'https://example.com/notifications'),
                    (2, '2020-02-18 20:00:00', 'https://example.com/search')
                ]
            )
    conn.commit()
    

# Day 12
# Problem statement:
# Given a table with event logs, find the top five users with the 
# longest continuous streak of visiting the platform in 2020.
# Note: A continuous streak counts if the user visits the platform 
# at least once per day on consecutive days.

table_name = "events"
# delete table if exists
delete_table(conn, cursor, table_name)
# create tables
command = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        user_id INTEGER,
        created_at DATETIME,
        url VARCHAR(300)
    )
"""
cursor.executescript(command)
conn.commit()

# add synthetic data
add_data()


command = f"""
with {table_name}_grouped as
(
    select user_id, date(created_at) created_date,
    row_number() over (partition by user_id order by date(created_at)) as rank_num  
    from {table_name} group by user_id, created_date
),
{table_name}_streak as
(   
    select user_id, date(created_date,  - rank_num || ' days') streak_s from {table_name}_grouped
),
{table_name}_streak_grouped as
(   
    select user_id, count(*) streak_len from {table_name}_streak group by user_id, streak_s
),
{table_name}_streak_grouped_len as
(   
    select user_id, max(streak_len) max_streak_len from {table_name}_streak_grouped group by user_id
)
select user_id, max_streak_len from {table_name}_streak_grouped_len order by max_streak_len desc
"""

# cursor.executescript(command)  
rows = select_data(cursor, command)
for row in rows:
    print(row)

