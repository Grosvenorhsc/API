import apicall
import database_utils
import parse_date

base_url = "https://grosvenorhsc.eploy.net/api/"

def get_placements():

    db = database_utils.Database()
    db.connect()

    class record:
        def __init__(self, PlacementId, StartDate, EndDate, PlacementStatus, Vacancy, Candidate, Salary, Salary_rate, CreationDate, ModificationDate ):
            self.PlacementId = PlacementId
            self.StartDate = StartDate
            self.EndDate = EndDate
            self.PlacementStatus = PlacementStatus
            self.Vacancy = Vacancy
            self.Candidate = Candidate
            self.Salary = Salary
            self.Salary_rate = Salary_rate
            self.CreationDate = CreationDate
            self.ModificationDate = ModificationDate

    api_url = base_url + "placements/search"  

    # Execute a SELECT statement
    results = db.query("SELECT COALESCE( (select CONVERT(NVARCHAR(26), max( P.ModificationDate), 126) + 'Z' FROM Placements P),  CONVERT(NVARCHAR(26), '2023/01/01T00:00:00Z', 26))as [date]")

    for row in results:
        filterdate = row[0]
        #filterdate = "2023/01/01T00:00:00Z"

    current_page = 1
    total_pages = 1  # Initialize to 1 to ensure the while loop runs at least on

    while current_page <= total_pages:
        body = {
            "Paging": {
                "RecordsPerPage": 100,
                "RequestedPage": current_page
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

        r = apicall.request(api_url, body, "POST")

        # Check if the 'TotalPages' field is present and update total_pages
        total_pages = r.get('TotalPages', 1)

        for placment in r['Records']:

            PlacementStatus_data = placment.get('PlacementStatus')
            PlacementStatus = 'None' if PlacementStatus_data is None else PlacementStatus_data.get('Description')

            Vacancy_data = placment.get('Vacancy')
            Vacancy = 'None' if Vacancy_data is None else Vacancy_data.get('Id')

            Candidate_data = placment.get('Candidate')
            Candidate = 'None' if Candidate_data is None else Candidate_data.get('Id')

            Salary_data = placment.get('Salary')
            Salary = 'None' if Salary_data is None else Salary_data.get('Salary')
            SalaryInterval = 'None' if Salary_data['SalaryInterval'] is None else Salary_data['SalaryInterval']['Description']

            p1 = record(
                str(placment.get("PlacementId")), 
                str(placment.get("StartDate")), 
                str(placment.get("EndDate")), 
                PlacementStatus, 
                Vacancy,
                Candidate,
                Salary,
                SalaryInterval,
                str(placment.get("CreationDate")),
                str(placment.get("ModificationDate"))
            )

            # Define the SQL INSERT statement
            sql_query = "INSERT INTO Temp_Placements (PlacementId,StartDate,EndDate,PlacementStatus,Vacancy,Candidate,Salary,Salary_rate,CreationDate,ModificationDate) VALUES (?,?,?,?,?,?,?,?,?,?);"

            db.query(sql_query, p1)
            db.commit()
        
        # Move to the next page
        current_page += 1

    # Define the SQL INSERT statement
    # Execute a SELECT statement
    results = db.query("SELECT COALESCE( (select CONVERT(NVARCHAR(26), max( P.ModificationDate), 126) + 'Z' FROM Placements P),  CONVERT(NVARCHAR(26), '2023/01/01T00:00:00Z', 26))as [date]")

    for row in results:
        filterdate = row[0]
        sql_query = "UPDATE table_updaterd SET last_run = ? WHERE table_name = 'Placements';"

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