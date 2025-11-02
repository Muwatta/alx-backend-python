#!/usr/bin/env python3
"""
1-batch_processing.py
- stream_users_in_batches(batch_size): yields batches (list of dicts)
- batch_processing(batch_size): yields or prints users over age 25
Max loops in code: <= 3 (we keep it simple)
"""

from seed import connect_to_prodev

def stream_users_in_batches(batch_size=50):
    """
    Generator that yields lists of rows (batches).
    Uses fetchmany to get batch_size rows per DB call.
    """
    conn = connect_to_prodev()
    if conn is None:
        return

    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT user_id, name, email, age FROM user_data")
        while True:
            rows = cursor.fetchmany(batch_size)
            if not rows:
                break
            # convert ages to int for consistency
            batch = [
                {
                    "user_id": r["user_id"],
                    "name": r["name"],
                    "email": r["email"],
                    "age": int(r["age"])
                } for r in rows
            ]
            yield batch
    finally:
        cursor.close()
        conn.close()


def batch_processing(batch_size=50):
    """
    Process each batch and print users with age > 25.
    This function uses the generator above.
    """
    for batch in stream_users_in_batches(batch_size):
        # one loop here (for each user in batch) - allowed within total loop budget
        for user in batch:
            if user["age"] > 25:
                print(user)
