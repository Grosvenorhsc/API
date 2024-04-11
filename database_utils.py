import pyodbc
import os
from dotenv import load_dotenv
import numpy as np  # Correcting the oversight
import re

class Database:
    def __init__(self, db_creds=None):
        if db_creds is None:
            db_creds = load_db_cred()
        self.db_creds = db_creds
        self.cnxn = None
        self.cursor = None

    def connect(self):
        try:
            self.cnxn = pyodbc.connect(
                DRIVER="{SQL Server}",
                SERVER=self.db_creds["Server"],
                DATABASE=self.db_creds["Database"],
                UID=self.db_creds["UID"],
                PWD=self.db_creds["PWD"]
            )
            self.cursor = self.cnxn.cursor()
        except pyodbc.Error as e:
            print("Error connecting to the SQL Server database:", e)
            exit()

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.cnxn:
            self.cnxn.close()

    def query(self, sql, params=None):
        if not self.cursor:
            self.connect()

         # Check if params is an instance of a class
        if params and not isinstance(params, (tuple, list)):
            # Extract attributes from the class instance
            params = tuple([getattr(params, attr) for attr in vars(params)])

        try:
            if params:
                paramitors = []
                regex_pattern = r'\b(?:nan|none)\b'

                # Loop through the properties of the record object
                for attr in params:
                    
                    match = None 

                    if type(attr) is str:
                        if len(attr) < 1:
                            attr = None
                        else:
                            # Check if the value matches the regex pattern for NaN or None
                            match = re.search(regex_pattern, attr, re.IGNORECASE)

                        # If the value matches the pattern, convert it to NULL
                        if match:
                            attr = None

                        # Append the parameter value to the list of parameters for the query
                        paramitors.append(attr)
                    else:
                        paramitors.append(attr)

                   
                self.cursor.execute(sql, paramitors)
            else:
                self.cursor.execute(sql)
                return self.cursor.fetchall()
        except pyodbc.Error as e:
            print("Error executing SQL query:", e)
            print("SQL:", sql)
            if params:
                print("Parameters:", params)
            raise e

    def commit(self):
        self.cnxn.commit()

def load_db_cred():
    print('Loading database credentials from .env file')
    load_dotenv()  # load environment variables from .env file
    
    db_creds = {
        "Server": os.getenv("DB_SERVER"),
        "Database": os.getenv("DB_NAME"),
        "UID": os.getenv("DB_USERNAME"),
        "PWD": os.getenv("DB_PASSWORD")
    }

    # Check if any credential is None and print a message before exiting.
    for key, value in db_creds.items():
        if value is None:
            print(f"Error: {key} is not set in the .env file.")
            exit()

    print('Database credentials loaded successfully')
    return db_creds