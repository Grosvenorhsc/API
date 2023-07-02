import apicall
import sql
import pyodbc
from datetime import datetime
from dateutil import parser
from dotenv import dotenv_values
import logging
import checkfile

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

# Define a class to hold application record data
def get_applications():
    class record:
        def __init__(self, ApplicationId, ApplicationDate, ApplicationType, InfluenceToApply, InfluenceToApplyDescription, Workflow, Placement, Candidate, Vacancy, CreationDate, ModificationDate):
            self.ApplicationId = checkfile.validate_parameters(str(ApplicationId).lower())
            self.ApplicationDate = checkfile.validate_parameters(str(ApplicationDate).lower())
            self.ApplicationType = checkfile.validate_parameters(str(ApplicationType).lower())
            self.InfluenceToApply = checkfile.validate_parameters(str(InfluenceToApply).lower())
            self.InfluenceToApplyDescription = checkfile.validate_parameters(str(InfluenceToApplyDescription).lower())
            self.Workflow = checkfile.validate_parameters(str(Workflow).lower())
            self.Placement = checkfile.validate_parameters(str(Placement).lower())
            self.Candidate = checkfile.validate_parameters(str(Candidate).lower())
            self.Vacancy = checkfile.validate_parameters(str(Vacancy).lower())
            self.CreationDate = checkfile.validate_parameters(str(CreationDate))
            self.ModificationDate = checkfile.validate_parameters(str(ModificationDate))

    # Set API URL for retrieving applications data
    api_url = base_url + "applications/search"

    # Execute a SELECT statement to retrieve the latest modification date
    result = cnxn.execute("SELECT COALESCE((SELECT TOP (1) CONVERT(NVARCHAR(26), last_run, 126) + 'Z' FROM table_updaterd WHERE table_name = 'Applications'), CONVERT(NVARCHAR(26), '2023/01/01T00:00:00Z', 26)) AS [date]")
    #result = cnxn.execute("SELECT CONVERT(NVARCHAR(26), '2023/01/01T00:00:00Z', 26) AS [date]")

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
        "ResponseBlocks":[
            "ApplicationId",
            "ApplicationDate",
            "ApplicationType",
            "InfluenceToApply",
            "InfluenceToApplyDescription",
            "Workflow",
            "Placement",
            "Candidate",
            "Vacancy",
            "Questions",
            "QuestionFields",
            "CreationDate",
            "ModificationDate"
        ]
    }

    # Set the pagination flag to True to retrieve all records
    paginated = True

    # Call the API to retrieve the applications data
    r = apicall.request(api_url, body, paginated)
    
    # Loop through each record in the API response
    for row in r:
        
        x = str(row.get("InfluenceToApplyDescription")).lower()
        y = str(x[0:47])
        
        # Create a new instance of the record class and populate it with the data from the API response
        p1 = record(
            str(row.get("ApplicationId")), 
            str(row.get("ApplicationDate")), 
            str(row.get("ApplicationType.Description")), 
            str(row.get("InfluenceToApply.Description")), 
            str(y),
            str(row.get("Workflow.Status.Description")),
            str(row.get("Placement.Id")),
            str(row.get("Candidate.Id")),
            str(row.get("Vacancy.Id")),
            str(row.get("CreationDate")),
            str(row.get("ModificationDate"))
        )

        # Log the company ID
        logging.info('Processed record: ApplicationId=%s', p1.ApplicationId)

        # Define the SQL query to insert the record into the database
        sql_query = "INSERT INTO Temp_Applications ([ApplicationId],[ApplicationDate],[ApplicationType],[InfluenceToApply],[InfluenceToApplyDescription],[Workflow],[Placement],[Candidate],[Vacancy],[CreationDate],[ModificationDate]) VALUES (?,?,?,?,?,?,?,?,?,?,?);"

        # Execute the SQL query to insert the record into the database
        sql.request(p1, sql_query)