import pyodbc
import re
import time
import logging
from dotenv import dotenv_values

# Load environment variables from .env file
config = dotenv_values('.env')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(filename)s - %(message)s',
    filename='project.log'
)

# Function to establish a connection to the SQL Server
def connect_to_database():
    try:
        cnxn = pyodbc.connect(
            DRIVER="{SQL Server}",
            SERVER=config["DB_SERVER"],
            DATABASE=config["DB_NAME"],
            UID=config["DB_USERNAME"],
            PWD=config["DB_PASSWORD"]
        )
        logging.info("Connected to the SQL Server database")
        return cnxn
    except pyodbc.Error as e:
        logging.error("Error connecting to the SQL Server database: %s", str(e))
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
            logging.info("Record inserted successfully")
            break  # Exit the loop if the query executed successfully
        except pyodbc.Error as e:
            if 'deadlock' in str(e).lower():
                logging.warning("Deadlock encountered. Retrying after 1 second...")
                retries += 1
                time.sleep(retry_delay)
            else:
                logging.error("Error executing the parameterized query: %s", str(e))
                break  # Exit the loop if the error is not a deadlock
