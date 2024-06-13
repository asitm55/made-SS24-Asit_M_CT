%%writefile test_pipeline.py

import sqlite3
import pytest

@pytest.fixture
def db_connection():
    # Connect to the SQLite database (replace with your database file name)
    connection = sqlite3.connect('your_database.db')
    yield connection
    connection.close()

def test_connection(db_connection):
    cursor = db_connection.cursor()
    cursor.execute("SELECT 1")
    assert cursor.fetchone() == (1,)

def test_table_exists(db_connection):
    cursor = db_connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='air_quality';")
    assert cursor.fetchone() is not None

def test_data_integrity(db_connection):
    cursor = db_connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM air_quality")
    count = cursor.fetchone()[0]
    assert count > 0

    cursor.execute("SELECT City FROM air_quality WHERE City='Visakhapatnam'")
    assert cursor.fetchone() is not None
