#!/usr/bin/python3
seed = __import__('seed')


def stream_user_ages():
    """Generator that yields one user age at a time."""
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT age FROM user_data")
    for row in cursor:  # loop 1
        yield row['age']
    connection.close()


def calculate_average():
    """Calculate average age using the generator."""
    total = 0
    count = 0
    for age in stream_user_ages():  # loop 2
        total += age
        count += 1
    if count == 0:
        return 0
    return total / count


if __name__ == "__main__":
    avg_age = calculate_average()
    print(f"Average age of users: {avg_age}")
