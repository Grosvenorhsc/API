import sql
import pyodbc
from datetime import datetime
from dateutil import parser
from dotenv import dotenv_values
import checkfile
import logging
import os

# Load environment variables from .env file
config = dotenv_values('.env')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(filename)s - %(message)s',
    filename='project.log'
)

# Set base URL for API calls
base_url = "https://grosvenorhsc.eploy.net/api/"

# Connect to SQL Server using the environment variables
cnxn = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={config["DB_SERVER"]};DATABASE={config["DB_NAME"]};UID={config["DB_USERNAME"]};PWD={config["DB_PASSWORD"]}')

# Define a class to hold company record data
def get_companies():
    class record:
        def __init__(self, CompanyId, ParentCompany, Name, CompanyStatus, CreationDate, ModificationDate):
            self.CompanyId = checkfile.validate_parameters(str(CompanyId).lower())
            self.ParentCompany = checkfile.validate_parameters(str(ParentCompany).lower())
            self.Name = checkfile.validate_parameters(str(Name).lower())
            self.CompanyStatus = checkfile.validate_parameters(str(CompanyStatus).lower())
            self.CreationDate = str(CreationDate)
            self.ModificationDate = str(ModificationDate)

    # Set API URL for retrieving company data
    api_url = base_url + "companies/search"

    # Set the filter parameters to retrieve all company records
    body = {
        "Paging": {
            "RecordsPerPage": 100,
            "RequestedPage": 1
        },
        "Filters": [

        ],
        "ResponseBlocks": [
            "CompanyId",
            "ParentCompany",
            "Name",
            "CompanyStatus",
            "CreationDate",
            "ModificationDate"
        ]
    }

    try:
        # Set the pagination flag to True to retrieve all records
        paginated = True

        # Call the API to retrieve the company data
        r = apicall.request(api_url, body, paginated)

        # Loop through each record in the response and insert into the SQL Server database
        for row in r:
            p1 = record(
                str(row.get("CompanyId")),
                str(row.get("ParentCompany.Id")),
                str(row.get("Name")),
                str(row.get("CompanyStatus.Description")),
                str(row.get("CreationDate")),
                str(row.get("ModificationDate"))
            )

            # Define the SQL query to insert the record into the database
            sql_query = "INSERT INTO Temp_Companies ([CompanyId],[ParentCompany],[Name],[CompanyStatus],[CreationDate],[ModificationDate]) VALUES (?,?,?,?,?,?);"

            # Execute the SQL query to insert the record into the database
            sql.request(p1, sql_query)

            # Log the company ID
            logging.info('Processed record: CompanyId=%s', p1.CompanyId)

    except Exception as e:
        # Log the error message
        logging.error('Error occurred: %s', str(e), exc_info=True)
