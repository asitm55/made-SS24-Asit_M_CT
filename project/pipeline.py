import os
import requests
import pandas as pd
import sqlite3

# Define the URL of the dataset
dataset_url = 'https://www.kaggle.com/datasets/shrutibhargava94/india-air-quality-data'

# Define the data directory
data_dir = 'data'
os.makedirs(data_dir, exist_ok=True)

# Fetch the dataset
response = requests.get(dataset_url)
dataset_path = os.path.join(data_dir, 'dataset.csv')

with open(dataset_path, 'wb') as file:
    file.write(response.content)

# Load the dataset into a DataFrame with error handling
try:
    df = pd.read_csv(dataset_path, on_bad_lines='skip')  # Skips bad lines
except pd.errors.ParserError as e:
    print(f"ParserError: {e}")
    # Additional handling if needed

# Data transformation and error fixing
# Example: Fill missing values and drop duplicates
df.fillna(method='ffill', inplace=True)
df.drop_duplicates(inplace=True)

# Define SQLite database path
db_path = os.path.join(data_dir, 'dataset.db')

# Save the DataFrame to SQLite
conn = sqlite3.connect(db_path)
df.to_sql('data', conn, if_exists='replace', index=False)
conn.close()

print(f"Data pipeline completed. Data is stored in {db_path}")
