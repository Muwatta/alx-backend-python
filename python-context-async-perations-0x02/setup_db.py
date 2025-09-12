import sqlite3

conn = sqlite3.connect('users.db')
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT,
    age INTEGER
)
''')
cursor.executemany('INSERT OR IGNORE INTO users (id, name, age) VALUES (?, ?, ?)',
                   [(1, 'Alice', 30), (2, 'Bob', 45), (3, 'Charlie', 25)])
conn.commit()
conn.close()