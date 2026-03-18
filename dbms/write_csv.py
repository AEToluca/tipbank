import os
import csv
from mysql import connector
from mysql.connector import Error

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

cursor = connection.cursor()
cursor.execute("SELECT * FROM testing")

rows = cursor.fetchall()
columns = [desc[0] for desc in cursor.description]

with open("testing.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(columns)  # Write column headers
    writer.writerows(rows)    # Write data

cursor.close()
connection.close()

print("CSV file created successfully.")