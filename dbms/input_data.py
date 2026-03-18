import os
from mysql import connector
from mysql.connector import Error

# Read credentials from environment variables (safer than hardcoding)
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_USER = os.getenv('DB_USER', 'AEToluca')
DB_PASSWORD = os.getenv('DB_PASSWORD', '04102810')
DB_DATABASE = os.getenv('DB_DATABASE', 'tipbank')

# Connect to MySQL once (reuse connection in this module)
try:
    connection = connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_DATABASE,
    )
    print("Connected to MySQL successfully.")
except Error as e:
    print('error connecting')
    raise

def execute_query(query, params=None, fetch=True, many=False, commit=False):
    """
    Execute a query safely and return results when requested.

    - query is the SQL statement with %s placeholders for parameters.
    - params is a tuple/list for execute or a list-of-tuples for executemany.
    - fetch controls whether to return rows (True for SELECT).
    - many uses executemany (for bulk inserts/updates).
    - commit commits the transaction (for INSERT/UPDATE/DELETE).
    """
    cursor = connection.cursor()

    try:
        if many:
            cursor.executemany(query, params or [])
        else:
            cursor.execute(query, params or ())

        if commit:
            connection.commit()

        if fetch:
            return cursor.fetchall()

        return None

    except Error as e:
        # Re-raise or handle logging here
        raise

    finally:
        cursor.close()

def parse_insertion(table_name, values):
    """Given the table to be inserted into and a list containing all the values to be inserted,
    parses the table and values into formatted basic insert query string""" 
    str_values = [f"'{v}'" if isinstance(v, str) else str(v) for v in values]
    r = "INSERT INTO " + table_name + " VALUES (" + ", ".join(str_values) + ");"
    return r

def insert_values(table, values):
    """Given a table and a list of values to be inserted, inserts the values into the table 
       assuming correct formatting."""
    try:
        cursor = connection.cursor()
        cursor.execute(parse_insertion(table, values))
        print(cursor.rowcount)
        connection.commit()
    except Error as e:
        raise
    finally:
        cursor.close()


def setup_user(admin_user='root', admin_password=None, target_user='AEToluca', target_password='04102810', host='127.0.0.1', database='tipbank'):
    """Setup MySQL user with privileges using admin credentials.
    
    Call this once with admin creds to create/grant the target user.
    """
    if not admin_password:
        admin_password = input("Enter admin password: ")
    
    admin_conn = connector.connect(
        host=host,
        user=admin_user,
        password=admin_password,
    )
    admin_cursor = admin_conn.cursor()
    try:
        # Create user if not exists
        admin_cursor.execute(f"CREATE USER IF NOT EXISTS '{target_user}'@'{host}' IDENTIFIED BY '{target_password}';")
        # Grant privileges
        admin_cursor.execute(f"GRANT ALL PRIVILEGES ON {database}.* TO '{target_user}'@'{host}';")
        admin_cursor.execute("FLUSH PRIVILEGES;")
        admin_conn.commit()
        print(f"User '{target_user}'@'{host}' created/granted on {database}.")
    except Error as e:
        print(f"Setup error: {e}")
        raise
    finally:
        admin_cursor.close()
        admin_conn.close()



if __name__ == "__main__":
    # Uncomment the next line to setup the user (requires admin password)
    # setup_user()
    test = [3, 21, 123.23, 30, 'CA', 'T']
    # Simple examples:
    # 1) SELECT all rows
    rows = execute_query("SELECT * FROM ticket;") 
    for r in rows or []: 
        print(r)
    
    
    #insert_values('ticket', test)

    # 2) Parameterized SELECT (safe against injection)
    # user_id = 1
    # rows = execute_query("SELECT * FROM testing WHERE id = %s;", (user_id,))

    # 3) INSERT example (remember to set commit=True)
    # insert_q = "INSERT INTO testing (name, value) VALUES (%s, %s);"
    # execute_query(insert_q, ("Alice", 123), fetch=False, commit=True)

    # Close connection when script ends
    connection.close()