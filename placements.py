import sql
from datetime import datetime
import pyodbc
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

# Connect to SQL Server using the environment variables
try:
    cnxn = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={config["DB_SERVER"]};DATABASE={config["DB_NAME"]};UID={config["DB_USERNAME"]};PWD={config["DB_PASSWORD"]}')
    logging.info('Connected to the database')
except Exception as e:
    logging.error('Failed to connect to the database: %s', str(e), exc_info=True)
    # Exit or handle the error appropriately

base_url = "https://grosvenorhsc.eploy.net/api/"

def get_placements():
    class record:
        def __init__(self, PlacementId, StartDate, EndDate, PlacementStatus, Vacancy, Candidate, Salary, Salary_rate, CreationDate, ModificationDate ):
            self.PlacementId = checkfile.validate_parameters(str(PlacementId).lower())
            self.StartDate = checkfile.validate_parameters(str(StartDate).lower())
            self.EndDate = checkfile.validate_parameters(str(EndDate).lower())
            self.PlacementStatus = checkfile.validate_parameters(str(PlacementStatus).lower())
            self.Vacancy = checkfile.validate_parameters(str(Vacancy).lower())
            self.Candidate = checkfile.validate_parameters(str(Candidate).lower())
            self.Salary = checkfile.validate_parameters(str(Salary).lower())
            self.Salary_rate = checkfile.validate_parameters(str(Salary_rate).lower())
            self.CreationDate = str(CreationDate)
            self.ModificationDate = str(ModificationDate)

    api_url = base_url + "placements/search"  

    # Execute a SELECT statement
    result = cnxn.execute("SELECT COALESCE( (select top (1) CONVERT(NVARCHAR(26), last_run, 126) + 'Z' FROM table_updaterd where table_name = 'Placements'),  CONVERT(NVARCHAR(26), '2023/01/01T00:00:00Z', 26))as [date]")

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
        {
            "Route": "Placement.ModificationDate",
            "Value": str(filterdate).replace("/","-"),
            "Operation": "GreaterThan"
        }
        ],
        "ResponseBlocks":[
            "PlacementId",
            "StartDate",
            "EndDate",
            "PlacementStatus",
            "Vacancy",
            "Candidate",
            "Salary",
            "CreationDate",
            "ModificationDate"
        ]
    }

    paginated = True

    r = apicall.request(api_url, body, paginated)

    for row in r:

        p1 = record(
            str(row.get("PlacementId")), 
            str(row.get("StartDate")), 
            str(row.get("EndDate")), 
            str(row.get("PlacementStatus.Description")), 
            str(row.get("Vacancy.Id")),
            str(row.get("Candidate.Id")),
            str(row.get("Salary.Salary")),
            str(row.get("Salary.SalaryInterval.Description")),
            str(row.get("CreationDate")),
            str(row.get("ModificationDate"))
        )

        # Log the company ID
        logging.info('Processed record: PlacementId=%s', p1.PlacementId)

        # Define the SQL INSERT statement
        sql_query = "INSERT INTO Temp_Placements (PlacementId,StartDate,EndDate,PlacementStatus,Vacancy,Candidate,Salary,Salary_rate,CreationDate,ModificationDate) VALUES (?,?,?,?,?,?,?,?,?,?);"

        sql.request(p1, sql_query)
