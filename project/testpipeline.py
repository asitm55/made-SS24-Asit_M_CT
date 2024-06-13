import os
import sqlite3
import pandas as pd

def test_file_existence():
    expected_files = ["air_quality_data.db"]
    for filepath in expected_files:
        assert os.path.isfile(filepath), f"File {filepath} does not exist."

def test_sqlite_tables():
    expected_tables = {
        "air_quality_data.db": ["air_quality"]
    }

    with sqlite3.connect('air_quality_data.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        existing_tables = [row[0] for row in cursor.fetchall()]
        for db_name, tables in expected_tables.items():
            for table in tables:
                assert table in existing_tables, f"Table {table} not found in {db_name}."

def test_data_integrity():
    expected_columns_types = {
        "air_quality": {
            "Timestamp": "object",
            "Year": "int64",
            "Month": "int64",
            "Day": "int64",
            "Hour": "int64",
            "PM2.5": "float64"
        }
    }

    with sqlite3.connect('air_quality_data.db') as conn:
        df_from_db = pd.read_sql_query("SELECT * FROM air_quality", conn)
        for table, columns_types in expected_columns_types.items():
            for column, expected_dtype in columns_types.items():
                assert column in df_from_db.columns, f"Column {column} not found in table {table}"
                assert str(df_from_db[column].dtype) == expected_dtype, f"Column {column} in table {table} has incorrect type {df_from_db[column].dtype}, expected {expected_dtype}"

if __name__ == "__main__":
    import pytest
    pytest.main(["-v", "--disable-warnings", "test_pipeline.py"])
