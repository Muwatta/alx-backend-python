import sqlite3

class ExecuteQuery:
    def __init__(self, query, param=None):
        self.query = query
        self.param = param
        self.conn = None
        self.cursor = None

    def __enter__(self):
        self.conn = sqlite3.connect('users.db')
        self.cursor = self.conn.cursor()
        if self.param:
            self.cursor.execute(self.query, (self.param,))
        else:
            self.cursor.execute(self.query)
        return self.cursor.fetchall()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

# Usage
result = ExecuteQuery("SELECT * FROM users WHERE age > ?", 25)
print(result.__enter__())
result.__exit__(None, None, None)