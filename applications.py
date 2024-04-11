import apicall             # Import the apicall module
from datetime import datetime  # Import the datetime module for working with dates and times
from dateutil import parser  # Import the parser module from dateutil for parsing dates
import database_utils
import parse_date

# Set base URL for API calls
base_url = "https://grosvenorhsc.eploy.net/api/"

# Define a class to hold application record data
def get_applications():

    db = database_utils.Database()
    db.connect()

    class record:
        def __init__(self, ApplicationId, ApplicationDate, ApplicationType, InfluenceToApply, InfluenceToApplyDescription, stage, status, Placement, Candidate, Vacancy, CreationDate, ModificationDate):
            self.ApplicationId = ApplicationId
            self.ApplicationDate = ApplicationDate
            self.ApplicationType = ApplicationType
            self.InfluenceToApply = InfluenceToApply
            self.InfluenceToApplyDescription = InfluenceToApplyDescription
            self.stage = stage
            self.status = status
            self.Placement = Placement
            self.Candidate = Candidate
            self.Vacancy = Vacancy
            self.CreationDate = CreationDate
            self.ModificationDate = ModificationDate

    # Set API URL for retrieving applications data
    api_url = base_url + "applications/search"

    # Execute a SELECT statement to retrieve the latest modification date
    results = db.query("SELECT COALESCE( (select CONVERT(NVARCHAR(26), max( C.ModificationDate), 126) + 'Z' FROM Applications C),  CONVERT(NVARCHAR(26), '2023/01/01T00:00:00Z', 26))as [date]")

    # Extract the latest modification date from the result set
    for row in results:
        filterdate = row[0]

    current_page = 1
    total_pages = 1  # Initialize to 1 to ensure the while loop runs at least once
    
    while current_page <= total_pages:
        # Set the filter parameters to retrieve only updated records since the latest modification date
        body = {
            "Paging": {
                "RecordsPerPage": 100,
                "RequestedPage": current_page
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

        # Call the API to retrieve the applications data
        r = apicall.request(api_url, body, "POST")

        # Check if the 'TotalPages' field is present and update total_pages
        total_pages = r.get('TotalPages', 1)
        
        # Loop through each record in the API response
        for application in r['Records']:
        
            x = str(application.get("InfluenceToApplyDescription"))
            y = str(x[0:47])

            ApplicationType_data = application.get('ApplicationType')
            ApplicationType = 'None' if ApplicationType_data is None else ApplicationType_data.get('Description')

            InfluenceToApply_data = application.get('InfluenceToApply')
            InfluenceToApply = 'None' if InfluenceToApply_data is None else InfluenceToApply_data.get('Description')

            Workflow_data = application.get('Workflow')
            Status = 'None' if Workflow_data['Status'] is None else Workflow_data['Status']['Description']
            Stage = 'None' if Workflow_data['Stage'] is None else Workflow_data['Stage']['Description']

            Placement_data = application.get('Placement')
            Placement = 'None' if Placement_data is None else Placement_data.get('Id')

            Candidate_data = application.get('Candidate')
            Candidate = 'None' if Candidate_data is None else Candidate_data.get('Id')

            Vacancy_data = application.get('Vacancy')
            Vacancy = 'None' if Vacancy_data is None else Vacancy_data.get('Id')
            
            # Create a new instance of the record class and populate it with the data from the API response
            p1 = record(
                str(application.get("ApplicationId")), 
                str(application.get("ApplicationDate")), 
                ApplicationType, 
                InfluenceToApply, 
                str(y),
                Stage,
                Status,
                Placement,
                Candidate,
                Vacancy,
                str(application.get("CreationDate")),
                str(application.get("ModificationDate"))
            )

            # Define the SQL query to insert the record into the database
            sql_query = "INSERT INTO Temp_Applications ([ApplicationId],[ApplicationDate],[ApplicationType],[InfluenceToApply],[InfluenceToApplyDescription],Stage,[status],[Placement],[Candidate],[Vacancy],[CreationDate],[ModificationDate]) VALUES (?,?,?,?,?,?,?,?,?,?,?,?);"
    
            db.query(sql_query, p1)
            db.commit()
        
        # Move to the next page
        current_page += 1
    
    results = db.query("SELECT COALESCE( (select CONVERT(NVARCHAR(26), max( C.ModificationDate), 126) + 'Z' FROM Applications C),  CONVERT(NVARCHAR(26), '2023/01/01T00:00:00Z', 26))as [date]")

    for row in results:
        filterdate = row[0]
        sql_query = "UPDATE table_updaterd SET last_run = ? WHERE table_name = 'Applications';"

        # Convert string to datetime object
        formats = ['%Y-%m-%dT%H:%M:%S.%fZ', '%Y-%m-%dT%H:%M:%SZ']
        dt = parse_date.parse_date(filterdate, formats)

        # Convert datetime object to string with desired format
        #formatted_date = dt.strftime('%Y/%m/%d')

        updatedate = []
        updatedate.append(dt)

        db.query(sql_query, updatedate)
        db.commit()
    
    db.close()