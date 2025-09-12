import mysql.connector
import csv
import uuid

def connect_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Generator10*#",
        )
        return connection
    except mysql.connector.Error:
        return None

def create_database(connection):
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
    cursor.close()

def connect_to_prodev():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Generator10*#",
            database="ALX_prodev"
        )
        return connection
    except mysql.connector.Error:
        return None

def create_table(connection):
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_data (
            user_id VARCHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL NOT NULL,
            INDEX idx_user_id (user_id)
        )
    """)
    print("Table user_data created successfully")
    cursor.close()

def insert_data(connection, file_path):
    cursor = connection.cursor()
    with open(file_path, 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip header
        for row in csv_reader:
            user_id = str(uuid.uuid4())
            cursor.execute("""
                INSERT INTO user_data (user_id, name, email, age)
                VALUES (%s, %s, %s, %s)
            """, (user_id, row[0], row[1], row[2]))
        connection.commit()
    cursor.close()