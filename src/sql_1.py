import sqlite3

import random 
from datetime import datetime, timedelta 

from utils import *

# Connect to (or create) a database file
conn = sqlite3.connect("sql_challenge.db")

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

def add_data():
    names = ["Alex", "Bob", "Peter"]
    for i in range(5):
        id = random.randint(1, 10)
        name = random.choice(names)
        cursor.execute(
                f"insert into users (user_id, name) values (?, ?)", (id, name)
            )
    conn.commit()
    
    command = "select user_id from users"
    user_ids = select_data(cursor, command)


    # add data to the events table
    actions = ["like", "comment", "post"]
    for i in range(20):
        user_id = random.choice(user_ids[:-1])
        action = random.choice(actions)
        timestamp = datetime.now() - timedelta(days=random.randint(0, 30), hours=random.randint(0, 23))
        cursor.execute(
            f"insert into events (user_id, action, timestamp) values (?, ?, ?)", (user_id[0], action, timestamp)
        )
    cursor.execute(
            f"insert into events (user_id, action, timestamp) values (?, ?, ?)", (user_ids[-1][0], "post", timestamp)
        )
    conn.commit()

# Day 1
# Problem statement:
# You’re given two tables: users and events. The events table holds values for all user activities in the action column — specifically ‘like’, ‘comment’, or ‘post’.
# Write a query to calculate the percentage of users who have never liked or commented, rounded to two decimal places.
# delete tables if exists
delete_table(conn, cursor, "users")
delete_table(conn, cursor, "events")
# create tables
command = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL, 
        name TEXT
    );
    CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        timestamp DATETIME NOT NULL,
        action TEXT CHECK(action IN ("post", "like", "comment")),
        FOREIGN KEY (user_id) REFERENCES users(user_id)

    )
"""
cursor.executescript(command)
conn.commit()

# add synthetic data
add_data()

command = """
SELECT *
from users where user_id not in (select user_id from events where action in ('like', 'comment'))
"""
rows = select_data(cursor, command)
for row in rows:
    print(row)

print("the row from users table")
rows = select_data(cursor, "select * from users")
for row in rows:
    print(row)
