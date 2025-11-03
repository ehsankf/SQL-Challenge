def delete_table(conn, cursor, table):
    # Drop the table (if it exists)
    cursor.execute(f"DROP TABLE IF EXISTS {table}")

    # Commit and close
    conn.commit()

def list_tables(cursor):
    # Get a list of all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

    tables = cursor.fetchall()

    print("Tables in database:")
    for table in tables:
        print(table[0])

def list_table_cols(cursor, table):
    cursor.execute(f"PRAGMA table_info({table})")
    columns = cursor.fetchall()
    for col in columns:
        print(f"name: {col[0]} type: {col[1]}")

def add_column(cursor, table_name, col_name, col_type):
    cursor.execute(f"alter table {table_name} add column {col_name} {col_type}")

def select_data(cursor, command):
    cursor.execute(command)

    rows = cursor.fetchall()
    return rows 