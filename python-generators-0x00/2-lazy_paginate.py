#!/usr/bin/python3
seed = __import__('seed')


def paginate_users(page_size, offset):
    """Fetch a page of users from the database."""
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    connection.close()
    return rows


def lazy_paginate(page_size):
    """Generator that lazily fetches pages of users."""
    offset = 0
    while True:  # only one loop
        rows = paginate_users(page_size, offset)
        if not rows:
            break
        yield rows
        offset += page_size
