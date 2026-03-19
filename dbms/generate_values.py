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
# Returns True if the given date was a double shift
def is_double_shift(day):
    cursor = connection.cursor()
    cursor.execute(
    "SELECT COUNT(shift_date) FROM shifts WHERE shift_date = %s",
    (day,))
    x = cursor.fetchone()
    if x[0] > 2:
        raise ValueError("More than 2 shifts found for a single day")
    elif x[0] == 2:
        return True
    else:
        return False
    
# Returns the total cash tips made given a date in mysql date data type format. If a double shift was worked return both values: (am, pm)
def total_cash_daily(day):
    cursor = connection.cursor()

    if is_double_shift(day):
        cursor.execute("""
            SELECT SUM(t.tip_amount)
            FROM ticket t
            LEFT JOIN shifts s ON t.shift_id = s.shift_id
            WHERE t.tip_type = 'CS' AND s.shift_date = %s AND s.period = 'AM'
        """, (day,))
        am_value = cursor.fetchone()[0] or 0

        cursor.execute("""
            SELECT SUM(t.tip_amount)
            FROM ticket t
            LEFT JOIN shifts s ON t.shift_id = s.shift_id
            WHERE t.tip_type = 'CS' AND s.shift_date = %s AND s.period = 'PM'
        """, (day,))
        pm_value = cursor.fetchone()[0] or 0

        result = (am_value, pm_value)

    else:
        cursor.execute("""
            SELECT SUM(t.tip_amount)
            FROM ticket t
            LEFT JOIN shifts s ON t.shift_id = s.shift_id
            WHERE t.tip_type = 'CS' AND s.shift_date = %s
        """, (day,))
        value = cursor.fetchone()[0] or 0
        result = value

    cursor.close()
    return result

# Returns the total credit tips made given a date in mysql date data type format. If a double shift was worked return both values: (am, pm)
def total_credit_daily(day):
    cursor = connection.cursor()

    if is_double_shift(day):
        cursor.execute("""
            SELECT SUM(t.tip_amount)
            FROM ticket t
            LEFT JOIN shifts s ON t.shift_id = s.shift_id
            WHERE t.tip_type = 'CR' AND s.shift_date = %s AND s.period = 'AM'
        """, (day,))
        am_value = cursor.fetchone()[0] or 0

        cursor.execute("""
            SELECT SUM(t.tip_amount)
            FROM ticket t
            LEFT JOIN shifts s ON t.shift_id = s.shift_id
            WHERE t.tip_type = 'CR' AND s.shift_date = %s AND s.period = 'PM'
        """, (day,))
        pm_value = cursor.fetchone()[0] or 0

        result = (am_value, pm_value)
    else:
        cursor.execute("""
            SELECT SUM(t.tip_amount)
            FROM ticket t
            LEFT JOIN shifts s ON t.shift_id = s.shift_id
            WHERE t.tip_type = 'CR' AND s.shift_date = %s
        """, (day,))
        value = cursor.fetchone()[0] or 0
        result = value

    cursor.close()
    return result

# Returns the total upngo tips made given a date in mysql date data type format. If a double shift was worked return both values: (am, pm)
def total_UPnGO_daily(day):
    cursor = connection.cursor()

    if is_double_shift(day):
        cursor.execute("""
            SELECT SUM(t.tip_amount)
            FROM ticket t
            LEFT JOIN shifts s ON t.shift_id = s.shift_id
            WHERE t.tip_type = 'UP' AND s.shift_date = %s AND s.period = 'AM'
        """, (day,))
        am_value = cursor.fetchone()[0] or 0

        cursor.execute("""
            SELECT SUM(t.tip_amount)
            FROM ticket t
            LEFT JOIN shifts s ON t.shift_id = s.shift_id
            WHERE t.tip_type = 'UP' AND s.shift_date = %s AND s.period = 'PM'
        """, (day,))
        pm_value = cursor.fetchone()[0] or 0

        result = (am_value, pm_value)
    else:
        cursor.execute("""
            SELECT SUM(t.tip_amount)
            FROM ticket t
            LEFT JOIN shifts s ON t.shift_id = s.shift_id
            WHERE t.tip_type = 'UP' AND s.shift_date = %s
        """, (day,))
        value = cursor.fetchone()[0] or 0
        result = value

    cursor.close()
    return result

# Returns the total tips made given a date in mysql date data type format. If a double shift was worked return both values: (am, pm)
def total_made(day):
    cursor = connection.cursor()
    if is_double_shift(day):
        cursor.execute("""
            SELECT SUM(t.tip_amount)
            FROM ticket t
            LEFT JOIN shifts s ON t.shift_id = s.shift_id
            WHERE s.shift_date = %s AND s.period = 'AM'
        """, (day,))
        am_value = cursor.fetchone()[0] or 0

        cursor.execute("""
            SELECT SUM(t.tip_amount)
            FROM ticket t
            LEFT JOIN shifts s ON t.shift_id = s.shift_id
            WHERE s.shift_date = %s AND s.period = 'PM'
        """, (day,))
        pm_value = cursor.fetchone()[0] or 0

        result = (am_value, pm_value)
    else:
        cursor.execute("""
            SELECT SUM(t.tip_amount)
            FROM ticket t
            LEFT JOIN shifts s ON t.shift_id = s.shift_id
            WHERE s.shift_date = %s
        """, (day,))
        value = cursor.fetchone()[0] or 0
        result = value

    cursor.close()
    return result

# Returns the average tips made given a date in mysql date data type format. If a double shift was worked return both values: (am, pm)
def average_daily(day):
    cursor = connection.cursor()
    if is_double_shift(day):
        cursor.execute("""
            SELECT AVG(tip_amount)
            FROM ticket t
            LEFT JOIN shifts s ON t.shift_id = s.shift_id
            WHERE s.shift_date = %s AND s.period = 'AM'
        """, (day,))
        am_value = cursor.fetchone()[0] or 0

        cursor.execute("""
            SELECT AVG(t.tip_amount)
            FROM ticket t
            LEFT JOIN shifts s ON t.shift_id = s.shift_id
            WHERE s.shift_date = %s AND s.period = 'PM'
        """, (day,))
        pm_value = cursor.fetchone()[0] or 0

        result = (am_value, pm_value)
    else:
        cursor.execute("""
            SELECT AVG(t.tip_amount)
            FROM ticket t
            LEFT JOIN shifts s ON t.shift_id = s.shift_id
            WHERE s.shift_date = %s
        """, (day,))
        value = cursor.fetchone()[0] or 0
        result = value

    cursor.close()
    return result

    def check_averages_daily(day):
        #todo. perhaps put each check into a dict or list. Use check_id as key and calculate average for value
        return

    
if __name__ == "__main__":
    # Uncomment the next line to setup the user (requires admin password)
    # setup_user()
    test = [3, 21, 123.23, 30, 'CA', 'T']
    # Simple examples:
    # 1) SELECT all rows
    print(is_double_shift('2024-10-28'))
    print(average_daily('2024-10-28'))