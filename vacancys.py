import apicall
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

# Protect database connection with try-except block
try:
    # Connect to SQL Server using the environment variables
    cnxn = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={config["DB_SERVER"]};DATABASE={config["DB_NAME"]};UID={config["DB_USERNAME"]};PWD={config["DB_PASSWORD"]}')
    logging.info('Connected to the database')
except Exception as e:
    # Log the error message
    logging.error('Failed to connect to the database: %s', str(e), exc_info=True)
    # Exit or handle the error appropriately

def get_vacancys():
    class record:
        def __init__(self, VacancyId, Title, VacancyStatus, Location, Company, Salary, CreationDate, ModificationDate):
            # Convert all data to string type and store in instance variables
            self.VacancyId = checkfile.validate_parameters(str(VacancyId).lower())
            self.Title = checkfile.validate_parameters(str(Title).lower())
            self.VacancyStatus = checkfile.validate_parameters(str(VacancyStatus).lower())
            self.Location = checkfile.validate_parameters(str(Location).lower())
            self.Company = checkfile.validate_parameters(str(Company).lower())
            self.Salary = checkfile.validate_parameters(str(Salary).lower())
            self.CreationDate = str(CreationDate)
            self.ModificationDate = str(ModificationDate)

    api_url = base_url + "vacancies/search"

    try:
        # Execute a SELECT statement
        result = cnxn.execute("SELECT COALESCE((SELECT TOP (1) CONVERT(NVARCHAR(26), last_run, 126) + 'Z' FROM table_updaterd WHERE table_name = 'Vacancies'), CONVERT(NVARCHAR(26), '2023/01/01T00:00:00Z', 26)) AS [date]")

        # Loop through the result set
        rows = result.fetchall()

        for row in rows:
            filterdate = row[0]

        body = {
            "Paging": {
                "RecordsPerPage": 100,
                "RequestedPage": 1
            },
            "Filters": [
                # {
                # "Route": "Placement.ModificationDate",
                # "Value": str(filterdate).replace("/", "-"),
                # "Operation": "GreaterThan"
                # }
            ],
            "ResponseBlocks": [
                "VacancyId",
                "Title",
                "VacancyStatus",
                "Location",
                "Company",
                "Salary",
                "CreationDate",
                "ModificationDate"
            ]
        }

        paginated = True

        r = apicall.request(api_url, body, paginated)

        for row in r:
            p1 = record(
                str(row.get("VacancyId")),
                str(row.get("Title")),
                str(row.get("VacancyStatus.Description")),
                str(row.get("Location.Description")),
                str(row.get("Company.Id")),
                str(row.get("Salary.Salary")),
                str(row.get("CreationDate")),
                str(row.get("ModificationDate"))
            )

            # Log the company ID
            logging.info('Processed record: VacancyId=%s', p1.VacancyId)

            # Define the SQL INSERT statement
            sql_query = "INSERT INTO Temp_Vacancys (VacancyId, Title, VacancyStatus, Location, Company, Salary, CreationDate, ModificationDate) VALUES (?, ?, ?, ?, ?, ?, ?, ?);"

            # Execute the SQL query to insert the record into the database
            sql.request(p1, sql_query)

            # Log the VacancyId
            logging.info('Processed record: VacancyId=%s', p1.VacancyId)

    except Exception as e:
        # Log the error message
        logging.error('Error occurred: %s', str(e), exc_info=True)
