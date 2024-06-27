import os
os.environ['KAGGLE_USERNAME'] = 'asit111' 
os.environ['KAGGLE_KEY'] = '9b8b0b2238108048307e7fb9a882db93' 

import kaggle
import time
import requests
import sqlite3
import pandas as pd
import shutil

import zipfile

def kaggle_download():

    dataset_links = ["https://www.kaggle.com/datasets/rohanrao/air-quality-data-in-india"]

    for dataset in dataset_links:
        folder_name = f"../data/{'-'.join(dataset.split('/')[-2:])}"
        dataset = '/'.join(dataset.split('/')[-2:])

        #print(f'Creating folder at {folder_name}')
        #os.mkdir(folder_name)

        print(f'Downloading the {dataset} dataset')

        kaggle.api.dataset_download_files(dataset, path="../data/downloads", unzip=True)
        
        print("File Saved to ../data/downloads")
        time.sleep(1)




def download_file(url, save_path):
    """
    Downloads a file from a given URL and saves it to a specified location.

    :param url: URL of the file to be downloaded
    :param save_path: Local path where the file will be saved
    """
    try:
        # Send a HTTP request to the URL
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Check if the request was successful

        # Open a local file with the same name as the URL's file
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192): 
                file.write(chunk)

        print(f"File downloaded successfully and saved to '{save_path}'")

        if save_path.endswith(".zip"):
            with zipfile.ZipFile(save_path, 'r') as zip_ref:
                print("Unzipping Files")
                zip_ref.extractall('/'.join(save_path.split('/')[0:-1]))
                
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")


def csv_to_sqlite(csv_directory, sqlite_db_path):
    # Connect to the SQLite database (it will be created if it doesn't exist)
    conn = sqlite3.connect(sqlite_db_path)
    cursor = conn.cursor()
    
    # Loop through all files in the directory
    for filename in os.listdir(csv_directory):
        if filename.endswith(".csv"):
            file_path = os.path.join(csv_directory, filename)
            table_name = os.path.splitext(filename)[0]
            
            # Read the CSV file into a DataFrame
            df = pd.read_csv(file_path)
            
            # Write the DataFrame to the SQLite database
            df.to_sql(table_name, conn, if_exists='replace', index=False)
            print(f"Table '{table_name}' created/updated from file '{filename}'")
    
    # Commit the changes and close the connection
    conn.commit()
    conn.close()
    print(f"All CSV files have been imported into '{sqlite_db_path}'")




urls = ["https://data.gov.in/files/ogdpv2dms/s3fs-public/datafile/Table-20.6-All_India_SYB2016_1.csv",
        "https://raw.githubusercontent.com/aqli-epic/aqli-update/main/data/country-spotlights/aqli_country_data_India.zip"
       ]
if not os.path.exists("../data/downloads"):
    os.mkdir('../data/downloads')
for url in urls:
    filename = url.split('/')[-1]
    path_to_save = '../data/downloads/'+filename
    download_file(url,path_to_save)

print("-----------------------")
print("Downloading Kaggle DataSet")
kaggle_download()

print("Download Completed")

print("Reading CSV files")
csv_directory = '../data/downloads'
sqlite_db_path = '../data/database2.sqlite'
print("Creating DB file")
csv_to_sqlite(csv_directory, sqlite_db_path)

shutil.rmtree('../data/downloads')

print("Task Completed")

