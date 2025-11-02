#!/usr/bin/env python3
"""
0-stream_users.py
- stream_users(): generator that yields one user row (as dict) at a time
Requirements: only one loop inside the generator
"""

from seed import connect_to_prodev
import mysql.connector

def stream_users():
    """
    Generator: yields rows one by one.
    Uses server-side cursor via buffered=False and fetchmany to avoid loading all rows.
    Only one loop used here (while True).
    """
    conn = connect_to_prodev()
    if conn is None:
        return

    # cursor with dictionary=True for dict rows
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT user_id, name, email, age FROM user_data")
        # fetchone in a while loop (single loop)
        row = cursor.fetchone()
        while row:
            yield {
                "user_id": row["user_id"],
                "name": row["name"],
                "email": row["email"],
                "age": int(row["age"])
            }
            row = cursor.fetchone()
    finally:
        cursor.close()
        conn.close()


# If run directly, print first 5 rows
if __name__ == "__main__":
    from itertools import islice
    for u in islice(stream_users(), 5):
        print(u)
