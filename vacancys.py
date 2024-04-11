import apicall
import database_utils
from datetime import datetime
import parse_date

# Set base URL for API calls
base_url = "https://grosvenorhsc.eploy.net/api/"
  
def get_vacancys():

    db = database_utils.Database()
    db.connect()

    class record:
        def __init__(self, VacancyId, Title, VacancyStatus, Location, Company, Salary, CreationDate, ModificationDate):
            # Convert all data to string type and store in instance variables
            self.VacancyId = int(VacancyId)
            self.Title = str(Title)
            self.VacancyStatus = str(VacancyStatus)
            self.Location = str(Location)
            self.Company = Company
            self.Salary = Salary
            self.CreationDate = CreationDate
            self.ModificationDate = ModificationDate

    api_url = base_url + "vacancies/search"

    results = db.query("SELECT COALESCE( (select CONVERT(NVARCHAR(26), max( V.ModificationDate), 126) + 'Z' FROM Vacancys V),  CONVERT(NVARCHAR(26), '2023/01/01T00:00:00Z', 26))as [date]")

    for row in results:
        filterdate = row[0]

    current_page = 1
    total_pages = 1  # Initialize to 1 to ensure the while loop runs at least once
    
    while current_page <= total_pages:
        body = {
            "Paging": {
                "RecordsPerPage": 100,
                "RequestedPage": current_page
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

        r = apicall.request(api_url, body, "POST")

        # Check if the 'TotalPages' field is present and update total_pages
        total_pages = r.get('TotalPages', 1)

        for row in r['Records']:

            VacancyStatus_data = row.get('VacancyStatus')
            VacancyStatus = 'None' if VacancyStatus_data is None else VacancyStatus_data.get('Description')

            Location_data = row.get('Location')
            Location = 'None' if Location_data is None else Location_data.get('Description')

            Company_data = row.get('Company')
            Company = 'None' if Company_data is None else Company_data.get('Id')

            Salary_data = row.get('Salary')
            Salary = 'None' if Salary_data is None else Salary_data.get('Salary')

            p1 = record(
                row.get("VacancyId"),
                row.get("Title"),
                VacancyStatus,
                Location,
                Company,
                Salary,
                row.get("CreationDate"),
                row.get("ModificationDate")
            )

            # Define the SQL INSERT statement
            sql_query = "INSERT INTO Temp_Vacancys (VacancyId, Title, VacancyStatus, Location, Company, Salary, CreationDate, ModificationDate) VALUES (?, ?, ?, ?, ?, ?, ?, ?);"

            # Execute the SQL query using the sql.request function
            db.query(sql_query, p1)
            db.commit()

        # Move to the next page
        current_page += 1

    results = db.query("SELECT COALESCE( (select CONVERT(NVARCHAR(26), max( V.ModificationDate), 126) + 'Z' FROM Vacancys V),  CONVERT(NVARCHAR(26), '2023/01/01T00:00:00Z', 26))as [date]")

    for row in results:
        filterdate = row[0]
        sql_query = "UPDATE table_updaterd SET last_run = ? WHERE table_name = 'Vacancys';"

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

