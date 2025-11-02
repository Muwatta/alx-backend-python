#!/usr/bin/python3
import mysql.connector
from mysql.connector import Error
import csv
import uuid
import os

def connect_db():
    """Connect to MySQL server (no database selected yet)."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root"
        )
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None


def create_database(connection):
    """Create ALX_prodev database if not exists."""
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")
    cursor.close()


def connect_to_prodev():
    """Connect to the ALX_prodev database."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="ALX_prodev"
        )
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None


def create_table(connection):
    """Create table user_data if not exists."""
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_data (
            user_id VARCHAR(255) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL NOT NULL
        );
    """)
    connection.commit()
    print("Table user_data created successfully")
    cursor.close()


def insert_data(connection, csvfile):
    """Insert CSV data into user_data table if not already exists."""
    cursor = connection.cursor()
    with open(csvfile, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            user_id = str(uuid.uuid4())
            cursor.execute(
                "INSERT INTO user_data (user_id, name, email, age) VALUES (%s, %s, %s, %s)",
                (user_id, row['name'], row['email'], row['age'])
            )
    connection.commit()
    cursor.close()
