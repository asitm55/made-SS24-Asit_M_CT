import os
import requests
import pandas as pd
import sqlite3

# Define the URLs of the datasets
dataset_urls = [
    'https://www.kaggle.com/datasets/rohanrao/air-quality-data-in-india',
    'https://www.kaggle.com/datasets/shrutibhargava94/india-air-quality-data'
]

# Define the data directory
data_dir = 'data'
os.makedirs(data_dir, exist_ok=True)

def fetch_and_process_dataset(url, dataset_name):
    # Fetch the dataset
    response = requests.get(url)
    dataset_path = os.path.join(data_dir, f'{dataset_name}.csv')

    with open(dataset_path, 'wb') as file:
        file.write(response.content)

    # Load the dataset into a DataFrame with error handling
    try:
        df = pd.read_csv(dataset_path, on_bad_lines='skip')  # Skips bad lines
    except pd.errors.ParserError as e:
        print(f"ParserError: {e}")
        return None

    # Data transformation and error fixing
    # Example: Fill missing values and drop duplicates
    df.fillna(method='ffill', inplace=True)
    df.drop_duplicates(inplace=True)

    return df

# Process both datasets
dataframes = []
for i, url in enumerate(dataset_urls):
    df = fetch_and_process_dataset(url, f'dataset{i+1}')
    if df is not None:
        dataframes.append(df)

# Define SQLite database path
db_path = os.path.join(data_dir, 'datasets.db')

# Save the DataFrames to SQLite
conn = sqlite3.connect(db_path)
for i, df in enumerate(dataframes):
    table_name = f'data{i+1}'
    df.to_sql(table_name, conn, if_exists='replace', index=False)
conn.close()

print(f"Data pipeline completed. Data is stored in {db_path}")


