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
                f"insert into {table_name1} ('id', 'name', 'birthdate') values (?, ?, ?)", 
                [
                    (1, 'Alice', '1985-05-15'),
                    (2, 'Bob', '1990-11-20'),
                    (3, 'Charlie', '2005-07-22'),
                    (4, 'David', '1988-11-30'),
                    (5, 'Eve', '2011-08-25'),
                    (6, 'Frank', '1995-02-14'),
                    (7, 'Grace', '1975-12-01')
                ]
            )
    cursor.executemany(
                f"insert into {table_name2} ('search_id', 'query', 'has_clicked', 'user_id', 'search_time') values (?, ?, ?, ?, ?)", 
                [
                    (1, 'travel', True, 1, '2021-03-15 10:00:00'),
                    (2, 'books', False, 2, '2021-03-20 11:00:00'),
                    (3, 'cars', True, 3, '2021-05-20 14:00:00'),
                    (4, 'tech', True, 3, '2021-05-20 15:00:00'),
                    (5, 'games', False, 4, '2021-06-20 16:00:00'),
                    (6, 'music', False, 5, '2021-07-25 12:00:00'),
                    (7, 'retirement', True, 6, '2021-09-05 09:15:00'),
                    (8, 'health', False, 7, '2021-09-05 15:00:00'),
                    (9, 'toys', False, 7, '2021-11-20 16:00:00'),
                    (10, 'genealogy', True, 1, '2021-12-01 11:50:00'),
                    (11, 'history', True, 2, '2021-12-01 12:00:00'),
                    (12, 'finance', True, 3, '2021-02-15 14:45:00'),
                    (13, 'investing', False, 4, '2021-02-15 09:00:00')
                ]
            )
    conn.commit()
    

# Day 13
# Problem statement:
# Given two tables, search_events and users, write a query to find the three age groups
#  (bucketed by decade: 0–9, 10–19, 20–29, …,80–89, 90–99, with the end point included) 
# with the highest clickthrough rate in 2021. If two or more groups have the same clickthrough
# rate, the older group should have priority.

# Hint: if a user that clicked the link on 1/1/2021 who is 29 years old on that day and
# has a birthday tomorrow on 2/1/2021, they fall into the [20–29] category. 
# If the same user clicked on another link on 2/1/2021, he turned 30 and will fall into the [30–39] category.

table_name1 = "users"
table_name2 = "search_events"
# delete table if exists
delete_table(conn, cursor, table_name1)
delete_table(conn, cursor, table_name2)

# create tables
command = f"""
    CREATE TABLE IF NOT EXISTS {table_name1} (
        id INTEGER PRIMARY KEY,
        name VARCHAR(50),
        birthdate DATETIME
    );
    CREATE TABLE IF NOT EXISTS {table_name2} (
        search_id INTEGER PRIMARY KEY,
        query VARCHAR(255),
        has_clicked BOOLEAN,
        user_id INTEGER,
        search_time DATETIME,
        FOREIGN KEY (user_id) REFERENCES {table_name1}(id)
    );
"""
cursor.executescript(command)
conn.commit()

# add synthetic data
add_data()


command = f"""
with {table_name1}_age as 
(
    select name, has_clicked, 
    strftime('%Y', search_time) -  strftime('%Y', birthdate) + (case when strftime('%m-%d', birthdate) < strftime('%m-%d', search_time) then 1 else 0 end) age 
    from {table_name2} t2 join {table_name1} t1 on t2.user_id=t1.id
),
{table_name1}_age_group as
(
    select name, has_clicked,
    (case when age <= 9 then '0–9' 
    when age <= 19 then '10–19'
    when age <= 29 then '20–29'
    when age <= 39 then '30–39'
    when age <= 49 then '40–49'
    when age <= 59 then '50–59'
    when age <= 69 then '60–69'
    when age <= 79 then '70–79'
    when age <= 89 then '80–89'
    else '90–99' end) as age_group
    from {table_name1}_age
)
select age_group, round(sum(case when has_clicked then 1 else 0 end)*1./count(*) * 100, 2) as ctr_percentage
from {table_name1}_age_group group by age_group order by ctr_percentage desc, age_group asc
"""
# cursor.executescript(command)  
rows = select_data(cursor, command)
for row in rows:
    print(row)

