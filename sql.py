import pyodbc
import re
import time
from dotenv import load_dotenv, find_dotenv
import os

# Find and load the .env file
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

# Function to establish a connection to the SQL Server
def connect_to_database():
    try:
        cnxn = pyodbc.connect(
            DRIVER="{SQL Server}",
            SERVER=os.getenv("DB_SERVER"),
            DATABASE=os.getenv("DB_NAME"),
            UID=os.getenv("DB_USERNAME"),
            PWD=os.getenv("DB_PASSWORD")
        )
        return cnxn
    except pyodbc.Error as e:
        raise

# Establish a connection to the SQL Server
cnxn = connect_to_database()

# Function to execute a parameterized query to insert records into the database
def request(record, sql, max_retries=3, retry_delay=1):
    params = []
    regex_pattern = r'\b(?:nan|none)\b'

    # Loop through the properties of the record object
    for attr, value in record.__dict__.items():
        # Convert empty strings to NULL
        if len(value) < 1:
            value = None
        else:
            # Check if the value matches the regex pattern for NaN or None
            match = re.search(regex_pattern, value, re.IGNORECASE)

            # If the value matches the pattern, convert it to NULL
            if match:
                value = None

        # Append the parameter value to the list of parameters for the query
        params.append(value)

    retries = 0
    while retries < max_retries:
        try:
            # Execute the parameterized query with the list of parameters
            cursor = cnxn.cursor()
            cursor.execute(sql, params)
            cnxn.commit()
            cursor.close()
            break  # Exit the loop if the query executed successfully
        except pyodbc.Error as e:
            if 'deadlock' in str(e).lower():
                retries += 1
                time.sleep(retry_delay)
            else:
                break  # Exit the loop if the error is not a deadlock
