import csv

from db import connection

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