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
                f"insert into {table_name1} (id, user_name) values (?, ?)", 
                [
                    (1, 'john_doe'),
                    (2, 'jane_smith'),
                    (3, 'bob_wilson')
                ]
            )
    cursor.executemany(
                f"insert into {table_name2} ('id', 'played_at', 'user_id', 'song_id') values (?, ?, ?, ?)", 
                [
                    (1, '2024-01-01 10:00:00', 1, 101),
                    (2, '2024-01-01 14:00:00', 1, 101),
                    (3, '2024-01-02 08:00:00', 2, 102),
                    (4, '2024-01-03 16:00:00', 3, 103),
                    (5, '2024-01-04 11:00:00', 3, 104),
                    (6, '2024-01-01 09:00:00', 2, 201),
                    (7, '2024-01-01 15:00:00', 2, 202),
                    (8, '2024-01-02 10:00:00', 3, 202),
                    (9, '2024-01-02 11:00:00', 3, 203),
                    (10, '2024-01-01 12:00:00', 3, 301),
                    (11, '2024-01-02 13:00:00', 3, 302)
                ]
            )
    conn.commit()
    

# Day 11
# Problem statement:
# Given a table of song_plays and a table of users, 
# write a query to extract the earliest date each user 
# played their third unique song and order by date played.

table_name1 = "users"
table_name2 = "song_plays"
# delete table if exists
delete_table(conn, cursor, table_name1)
delete_table(conn, cursor, table_name2)
# create tables
command = f"""
    CREATE TABLE IF NOT EXISTS {table_name1} (
        id INTEGER PRIMARY KEY,
        user_name VARCHAR(50)
    );
    CREATE TABLE IF NOT EXISTS {table_name2} (
        id INTEGER PRIMARY KEY,
        played_at DATETIME,
        user_id INTEGER,
        song_id INTEGER
    );
"""
cursor.executescript(command)
conn.commit()

# add synthetic data
add_data()


command = f"""
with {table_name2}_songs as 
(
    select user_id, song_id, min(played_at) as first_time_played
    from {table_name2}
    group by user_id, song_id
),
{table_name2}_rank as 
(
    select user_id, song_id, row_number() over (partition by user_id order by first_time_played) as ranking, first_time_played
    from {table_name2}_songs
)

select user_name, song_id, first_time_played from {table_name2}_rank t1 join {table_name1} t2 on t1.user_id=t2.id where ranking=3
"""
# cursor.executescript(command)  
rows = select_data(cursor, command)
for row in rows:
    print(row)

