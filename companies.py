from datetime import datetime
import apicall
import database_utils
import parse_date

# Set base URL for API calls
base_url = "https://grosvenorhsc.eploy.net/api/"

# Define a class to hold company record data
def get_companies():

    db = database_utils.Database()
    db.connect()

    class record:
        def __init__(self, CompanyId, ParentCompany, Name, CompanyStatus, CreationDate, ModificationDate):
            self.CompanyId = int(CompanyId)

            try:
                # If ParentCompany can be converted to float and is not 'nan'
                if ParentCompany != 'nan':
                    self.ParentCompany = ParentCompany
                else:
                    self.ParentCompany = None
            except ValueError:
                # Handle case where ParentCompany can't be converted to float
                self.ParentCompany = None

            self.Name = str(Name)
            self.CompanyStatus = str(CompanyStatus)
            self.CreationDate = CreationDate
            self.ModificationDate = ModificationDate

    # Set API URL for retrieving company data
    api_url = base_url + "companies/search"

    # Execute a SELECT statement
    results = db.query("SELECT COALESCE( (select CONVERT(NVARCHAR(26), max( C.ModificationDate), 126) + 'Z' FROM Companies C),  CONVERT(NVARCHAR(26), '2023/01/01T00:00:00Z', 26))as [date]")

    for row in results:
        filterdate = row[0]

    current_page = 1
    total_pages = 1  # Initialize to 1 to ensure the while loop runs at least once
    
    while current_page <= total_pages:

        # Set the filter parameters to retrieve all company records
        body = {
            "Paging": {
                "RecordsPerPage": 100,
                "RequestedPage": current_page
            },
            "Filters": [
                # {
                #     "Route": "Company.ModificationDate",
                #     "Value": str(filterdate).replace("/", "-"),
                #     "Operation": "GreaterThan"
                # }
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

        # Call the API to retrieve the company data
        r = apicall.request(api_url, body, "POST")

        # Check if the 'TotalPages' field is present and update total_pages
        total_pages = r.get('TotalPages', 1)

        # Loop through each record in the response and insert into the SQL Server database
        for row in r['Records']:

            ParentCompany_data = row.get('ParentCompany')
            ParentCompany = 'None' if ParentCompany_data is None or CompanyStatus_data is 'None' else ParentCompany_data.get('Id')

            CompanyStatus_data = row.get('CompanyStatus')
            CompanyStatus = 'None' if CompanyStatus_data is None or CompanyStatus_data is 'None' else CompanyStatus_data.get('Description')

            p1 = record(
                str(row.get("CompanyId")),
                ParentCompany,
                str(row.get("Name")),
                CompanyStatus,
                str(row.get("CreationDate")),
                str(row.get("ModificationDate"))
            )

            # Define the SQL query to insert the record into the database
            sql_query = "INSERT INTO Temp_Companies ([CompanyId],[ParentCompany],[Name],[CompanyStatus],[CreationDate],[ModificationDate]) VALUES (?,?,?,?,?,?);"

            db.query(sql_query, p1)
            db.commit()
                    
        # Move to the next page
        current_page += 1
        
    results = db.query("SELECT COALESCE( (select CONVERT(NVARCHAR(26), max( C.ModificationDate), 126) + 'Z' FROM Companies C),  CONVERT(NVARCHAR(26), '2023/01/01T00:00:00Z', 26))as [date]")

    for row in results:
        filterdate = row[0]
        sql_query = "UPDATE table_updaterd SET last_run = ? WHERE table_name = 'Companies';"

        # Convert string to datetime object
        formats = ['%Y-%m-%dT%H:%M:%S.%fZ', '%Y-%m-%dT%H:%M:%SZ']
        dt = parse_date.parse_date(filterdate, formats)

        # Convert datetime object to string with desired format
        formatted_date = dt.strftime('%Y-%m-%d')

        updatedate = []
        updatedate.append(formatted_date)

        db.query(sql_query, updatedate)
        db.commit()
    
    db.close()
        