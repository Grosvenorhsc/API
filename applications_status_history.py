import apicall             # Import the apicall module
import sql                 # Import the sql module
import pyodbc              # Import the pyodbc library for connecting to SQL Server
from datetime import datetime  # Import the datetime module for working with dates and times
from dateutil import parser  # Import the parser module from dateutil for parsing dates
import checkfile           # Import the checkfile module
from dotenv import load_dotenv, find_dotenv
import os

# Find and load the .env file
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

# Connect to SQL Server using the environment variables
cnxn = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={os.getenv("DB_SERVER")};DATABASE={os.getenv("DB_NAME")};UID={os.getenv("DB_USERNAME")};PWD={os.getenv("DB_PASSWORD")}')

# Set base URL for API calls
base_url = "https://grosvenorhsc.eploy.net/api/"

def get_status_history():
    class record:
        def __init__(self, StatusHistoryId, Application, Vacancy, Workflow, CreationDate, ModificationDate):
            self.StatusHistoryId = checkfile.validate_parameters(str(StatusHistoryId).lower())
            self.Application = checkfile.validate_parameters(str(Application).lower())
            self.Vacancy = checkfile.validate_parameters(str(Vacancy).lower())
            self.Workflow = checkfile.validate_parameters(str(Workflow).lower())
            self.CreationDate = str(CreationDate)
            self.ModificationDate = str(ModificationDate)

    # Set API URL for retrieving applications data
    api_url = base_url + "applications/statushistory/search"

    # Execute a SELECT statement to retrieve the latest modification date
    result = cnxn.execute("SELECT COALESCE((SELECT TOP (1) CONVERT(NVARCHAR(26), last_run, 126) + 'Z' FROM table_updaterd WHERE table_name = 'statushistory'), CONVERT(NVARCHAR(26), '2023/01/01T00:00:00Z', 26)) AS [date]")

    # Fetch all the rows from the result set
    rows = result.fetchall()

    # Extract the latest modification date from the result set
    for row in rows:
        filterdate = row[0]

    # Set the filter parameters to retrieve only updated records since the latest modification date
    body = {
        "Paging": {
            "RecordsPerPage": 100,
            "RequestedPage": 1
        },
        "Filters": [
            {
                "Route": "Application.ModificationDate",
                "Value": str(filterdate).replace("/", "-"),
                "Operation": "GreaterThan"
            }
        ],
        "ResponseBlocks": [
            "StatusHistoryId",
            "Application",
            "Vacancy",
            "Action",
            "Placement",
            "StatusDate",
            "Workflow",
            "CreationDate",
            "ModificationDate"
        ]
    }

    # Set the pagination flag to True to retrieve all records
    paginated = True

    # Call the API to retrieve the applications data
    r = apicall.request(api_url, body, paginated)

    for row in r:
        p1 = record(
            str(row.get("StatusHistoryId")),
            str(row.get("Application.Id")),
            str(row.get("Vacancy.Id")),
            str(row.get("Workflow.Stage.Description")),
            str(row.get("CreationDate")),
            str(row.get("ModificationDate"))
        )

        # Define the SQL query to insert the record into the database
        sql_query = "INSERT INTO Temp_statushistory ([StatusHistoryId],[Application_Id],[Vacancy_Id],[Application_stage_decription],[CreationDate],[ModificationDate]) VALUES (?,?,?,?,?,?);"

        # Execute the SQL query to insert the record into the database
        sql.request(p1, sql_query)

# Call the function
get_status_history()
