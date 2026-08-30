from db import connection
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

# Returns a dict of {check_id: tip_percentage} for the given day
def tip_percentages_daily(day):
    cursor = connection.cursor()
    cursor.execute("""
                   SELECT check_id, (t.tip_amount / t.bill_before_tip) * 100 as tip_percentage
                   FROM ticket t
                   JOIN shifts s ON t.shift_id = s.shift_id
                   WHERE s.shift_date = %s
                   """, (day,))
    result = {check_id: tip_percentage for check_id, tip_percentage in cursor.fetchall()}
    cursor.close()
    return result

def show_all_ticket():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM ticket")
    result = cursor.fetchall()
    cursor.close()
    return result



    
if __name__ == "__main__":
    # Uncomment the next line to setup the user (requires admin password)
    # setup_user()
    test = [3, 21, 123.23, 30, 'CA', 'T']
    # Simple examples:
    # 1) SELECT all rows
    print(is_double_shift('2024-10-28'))
    print(average_daily('2024-10-28'))
    print(tip_percentages_daily('2024-10-28'))
    print(show_all_ticket())
    