from db import connection

def monthly_summary(year=None):
    cursor = connection.cursor()
    query = """
        SELECT
            YEAR(s.shift_date) AS yr,
            MONTH(s.shift_date) AS mo,
            SUM(CASE WHEN t.tip_type = 'CS' THEN t.tip_amount ELSE 0 END) AS total_cash,
            SUM(CASE WHEN t.tip_type = 'CR' THEN t.tip_amount ELSE 0 END) AS total_credit,
            SUM(CASE WHEN t.tip_type = 'UP' THEN t.tip_amount ELSE 0 END) AS total_upngo,
            SUM(t.tip_amount) AS total_tips,
            AVG(t.tip_amount) AS avg_per_ticket,
            COUNT(DISTINCT s.shift_id) AS shifts_worked
        FROM ticket t
        JOIN shifts s ON t.shift_id = s.shift_id
    """
    params = ()
    if year:
        query += " WHERE YEAR(s.shift_date) = %s"
        params = (year,)
    query += " GROUP BY yr, mo ORDER BY yr, mo"

    cursor.execute(query, params)
    result = cursor.fetchall()
    cursor.close()
    return result


def yearly_summary():
    cursor = connection.cursor()
    cursor.execute("""
        SELECT
            YEAR(s.shift_date) AS yr,
            SUM(CASE WHEN t.tip_type = 'CS' THEN t.tip_amount ELSE 0 END) AS total_cash,
            SUM(CASE WHEN t.tip_type = 'CR' THEN t.tip_amount ELSE 0 END) AS total_credit,
            SUM(CASE WHEN t.tip_type = 'UP' THEN t.tip_amount ELSE 0 END) AS total_upngo,
            SUM(t.tip_amount) AS total_tips,
            AVG(t.tip_amount) AS avg_per_ticket,
            COUNT(DISTINCT s.shift_id) AS shifts_worked
        FROM ticket t
        JOIN shifts s ON t.shift_id = s.shift_id
        GROUP BY yr
        ORDER BY yr
    """)
    result = cursor.fetchall()
    cursor.close()
    return result


if __name__ == "__main__":
    rows = yearly_summary()
    if not rows:
        print("No yearly summary rows.")
    else:
        print(f"{'Year':<6} {'Cash':>10} {'Credit':>10} {'UPNGO':>10} {'Total':>10} {'Avg/ticket':>12} {'Shifts':>8}")
        for yr, cash, credit, upngo, total, avg, shifts in rows:
            print(
                f"{yr:<6} {cash:>10.2f} {credit:>10.2f} {upngo:>10.2f} "
                f"{total:>10.2f} {avg:>12.2f} {shifts:>8}"
            )
    connection.close()