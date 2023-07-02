# Import necessary libraries
import apicall
import sql
import sql
import pyodbc
from datetime import datetime
from dateutil import parser

# Set base URL for API calls
base_url = "https://grosvenorhsc.eploy.net/api/"

# Connect to SQL Server
cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=REPORTING\HEVO;DATABASE=Eploy;UID=HEVO;PWD=s1Licon3918$')

# Define a class to hold application record data
def get_actions():
    # class record:
    #     def __init__(self, ApplicationId, ApplicationDate, ApplicationType, InfluenceToApply, InfluenceToApplyDescription, Workflow, Placement, Candidate, Vacancy, CreationDate, ModificationDate):
    #         self.ApplicationId = str(ApplicationId).lower()
    #         self.ApplicationDate = str(ApplicationDate).lower()
    #         self.ApplicationType = str(ApplicationType).lower()
    #         self.InfluenceToApply = str(InfluenceToApply).lower()
    #         self.InfluenceToApplyDescription = str(InfluenceToApplyDescription).lower()
    #         self.Workflow = str(Workflow).lower()
    #         self.Placement = str(Placement).lower()
    #         self.Candidate = str(Candidate).lower()
    #         self.Vacancy = str(Vacancy).lower()
    #         self.CreationDate = str(CreationDate)
    #         self.ModificationDate = str(ModificationDate)

    # Set API URL for retrieving applications data
    api_url = base_url + "actions/search"

    # # Execute a SELECT statement to retrieve the latest modification date
    # result = cnxn.execute("SELECT COALESCE((SELECT TOP (1) CONVERT(NVARCHAR(26), last_run, 126) + 'Z' FROM table_updaterd WHERE table_name = 'Applications'), CONVERT(NVARCHAR(26), '2023/01/01T00:00:00Z', 26)) AS [date]")
    # #result = cnxn.execute("SELECT CONVERT(NVARCHAR(26), '2023/01/01T00:00:00Z', 26) AS [date]")

    # # Fetch all the rows from the result set
    # rows = result.fetchall()

    # # Extract the latest modification date from the result set
    # for row in rows:
    #     filterdate = row[0]

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
            "ActionId",
            "StartDate",
            "EndDate",
            "CompletionDate",
            "ActionOutcome",
            "ActionPriority",
            "Vacancy",
            "Candidate",
            "Vacancy",
            "CreationDate",
            "ModificationDate"
        ]
    }

    # Set the pagination flag to True to retrieve all records
    paginated = True

    # Call the API to retrieve the applications data
    r = apicall.request(api_url, body, paginated)
    print(r)
    # # Loop through each record in the API response
    # for row in r:
        
    #     x = str(row.get("InfluenceToApplyDescription")).lower()
    #     y = str(x[0:47])
        
    #     # Create a new instance of the record class and populate it with the data from the API response
    #     p1 = record(
    #         str(row.get("ApplicationId")), 
    #         str(row.get("ApplicationDate")), 
    #         str(row.get("ApplicationType.Description")), 
    #         str(row.get("InfluenceToApply.Description")), 
    #         str(y),
    #         str(row.get("Workflow.Status.Description")),
    #         str(row.get("Placement.Id")),
    #         str(row.get("Candidate.Id")),
    #         str(row.get("Vacancy.Id")),
    #         str(row.get("CreationDate")),
    #         str(row.get("ModificationDate"))
    #     )

    #     # Define the SQL query to insert the record into the database
    #     sql_query = "INSERT INTO Temp_Applications ([ApplicationId],[ApplicationDate],[ApplicationType],[InfluenceToApply],[InfluenceToApplyDescription],[Workflow],[Placement],[Candidate],[Vacancy],[CreationDate],[ModificationDate]) VALUES (?,?,?,?,?,?,?,?,?,?,?);"

    #     # Execute the SQL query to insert the record into the database
    #     sql.request(p1, sql_query)