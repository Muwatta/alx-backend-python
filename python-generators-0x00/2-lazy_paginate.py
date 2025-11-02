#!/usr/bin/env python3
"""
2-lazy_paginate.py
- lazy_pagination(page_size): generator yielding pages (lists of dicts)
- paginate_users(page_size, offset): helper (per project spec)
Only one loop inside the main generator.
"""

from seed import connect_to_prodev

def paginate_users(page_size, offset):
    conn = connect_to_prodev()
    if conn is None:
        return []
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(f"SELECT user_id, name, email, age FROM user_data LIMIT %s OFFSET %s", (page_size, offset))
        rows = cursor.fetchall()
        return rows
    finally:
        cursor.close()
        conn.close()


def lazy_pagination(page_size=100):
    """
    Generator that fetches the next page only when requested.
    Single loop: while True
    """
    offset = 0
    while True:
        rows = paginate_users(page_size, offset)
        if not rows:
            break
        page = [
            {"user_id": r["user_id"], "name": r["name"], "email": r["email"], "age": int(r["age"])}
            for r in rows
        ]
        yield page
        offset += page_size
