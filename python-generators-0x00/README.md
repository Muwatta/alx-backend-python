# Python Generators Project

This project demonstrates the use of Python generators for efficient data processing with a MySQL database.

## Files
- `seed.py`: Sets up MySQL database `ALX_prodev`, creates `user_data` table, and populates it with data from `user_data.csv`.
- `0-stream_users.py`: Generator to stream rows from `user_data` table one by one.
- `1-batch_processing.py`: Generator to fetch and process data in batches, filtering users over 25.
- `2-lazy_paginate.py`: Generator for lazy loading paginated data from `user_data` table.
- `4-stream_ages.py`: Generator to compute memory-efficient average age of users.

## Setup
1. Install MySQL and Python.
2. Install `mysql-connector-python`: `pip install mysql-connector-python`.
3. Ensure `user_data.csv` is available for seeding.
4. Update database credentials in `seed.py` if necessary.

## Usage
Run the main scripts (`0-main.py`, `1-main.py`, `2-main.py`, `3-main.py`) to test the functionality.

## Repository
- **GitHub**: alx-backend-python
- **Directory**: python-generators-0x00