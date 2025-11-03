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
                f"insert into {table_name} (user_id, created_at, action) values (?, ?, ?)", 
                [
                    (1, '2020-01-01 10:00:00', 'post_enter'),
                    (1, '2020-01-01 10:10:00', 'post_submit'),
                    (2, '2020-01-01 11:00:00', 'post_enter'),
                    (2, '2020-01-01 11:10:00', 'post_canceled'),
                    (3, '2020-01-01 15:00:00', 'post_enter'),
                    (3, '2020-01-01 15:30:00', 'post_submit'),
                    (4, '2020-01-02 09:00:00', 'post_enter'),
                    (4, '2020-01-02 09:15:00', 'post_canceled'),
                    (5, '2020-01-02 10:00:00', 'post_enter'),
                    (5, '2020-01-02 10:10:00', 'post_canceled'),
                    (10, '2020-01-15 14:00:00', 'post_enter'),
                    (10, '2020-01-15 14:30:00', 'post_submit'),
                    (6, '2019-12-31 23:45:00', 'post_enter'),
                    (6, '2020-01-01 00:05:00', 'post_submit'),
                    (7, '2020-02-01 00:00:00', 'post_enter'),
                    (7, '2020-02-01 00:10:00', 'post_submit'),
                    (8, '2019-01-15 10:00:00', 'post_enter'),
                    (8, '2019-01-15 10:30:00', 'post_submit'),
                    (9, '2021-01-01 09:00:00', 'post_enter'),
                    (9, '2021-01-01 09:10:00', 'post_canceled')
                ]
            )
    conn.commit()
    

# Day 5
# Problem statement:
# Consider the events table consisting of phases of posting a new social media post. 
# The action consists of values for when the user starts to write (enter_post), cancel 
# the post (cancel_post) or submit the post (submit_post). 
# Write a query to get the post success rate for each day in the month of January 2020. 
# Post success rate is defined by the number of the posts submitted divided the post entered for each day. 

table_name = "events"
# delete table if exists
delete_table(conn, cursor, table_name)
# create tables
command = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        user_id INTEGER,
        created_at DATETIME NOT NULL,
        action VARCHAR(50)
    )
"""
cursor.executescript(command)
conn.commit()

# add synthetic data
add_data()


command = f"""
with {table_name}_2020 as 
(
    select * from {table_name} where created_at between '2020-01-01' and '2020-01-31' and action in ('post_submit', 'post_canceled')
), 
{table_name}_join as (
    select e1.user_id, e2.created_at, e1.action, row_number() over (partition by e1.created_at order by e2.created_at desc) as ranking from {table_name}_2020 e1
    join {table_name} e2  
    on e1.user_id=e2.user_id and e2.action='post_enter' and e1.created_at > e2.created_at and e2.created_at >= '2020-01-01'
)
select date(created_at), count(*) as total_submit, 
sum(case when action='post_submit' then 1 else 0 end) as submit_total, 
round(sum(case when action='post_submit' then 1 else 0 end) * 1./nullif(count(*), 0), 2) * 100 as percent 
from {table_name}_join where ranking=1 group by date(created_at)
"""

# cursor.executescript(command)  
rows = select_data(cursor, command)
for row in rows:
    print(row)

