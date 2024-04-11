import apicall             # Import the apicall module 
from datetime import datetime  # Import the datetime module for working with dates and times
import database_utils
import parse_date

# Set base URL for API calls
base_url = "https://grosvenorhsc.eploy.net/api/"
    
def get_candidates():

    db = database_utils.Database()
    db.connect()

    class record:
        def __init__(self, CandidateId, Title, FirstName, Surname, Address1, Address2, Town, County, Country, PostCode, Telephone, Mobile, Email, Gender, CriminalRecord, WorkPermit, WorkPermitType, PreferredLocation1, IsEmployee, IsPreviousEmployee, CreationDate, ModificationDate):
            # Convert all data to string type and store in instance variables
            self.CandidateId = CandidateId
            self.Title = str(Title)[:50]
            self.FirstName = str(FirstName)[:50]
            self.Surname = str(Surname)[:50]
            self.Address1 = str(Address1)[:50]
            self.Address2 = str(Address2)[:50]
            self.Town = str(Town)[:50]
            self.County = str(County)[:50]
            self.Country = str(Country)[:50]
            self.PostCode = str(PostCode)[:50]
            self.Telephone = str(Telephone)[:50]
            self.Mobile = str(Mobile)[:50]
            self.Email = str(Email)[:50]
            self.Gender = str(Gender)[:50]
            self.CriminalRecord = str(CriminalRecord)[:50]
            self.WorkPermit = str(WorkPermit)[:50]
            self.WorkPermitType = str(WorkPermitType)[:50]
            self.PreferredLocation1 = str(PreferredLocation1)[:50]
            self.IsEmployee = str(IsEmployee)[:50]
            self.IsPreviousEmployee = str(IsPreviousEmployee)[:50]
            self.CreationDate = str(CreationDate)
            self.ModificationDate = str(ModificationDate)

    api_url = base_url + "candidates/search"
    
    # Execute a SELECT statement
    results = db.query("SELECT COALESCE( (select CONVERT(NVARCHAR(26), max( C.ModificationDate), 126) + 'Z' FROM Candidates C),  CONVERT(NVARCHAR(26), '2023/01/01T00:00:00Z', 26))as [date]")

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
                {
                    "Route": "Candidate.ModificationDate",
                    "Value": str(filterdate).replace("/", "-"),
                    "Operation": "GreaterThan"
                }
            ],
            "ResponseBlocks": [
                "CandidateId", "Title", "FirstName", "Surname", "Address",
                "Telephone", "Mobile", "Email", "Gender", "CriminalRecord",
                "WorkPermit", "WorkPermitType", "PreferredLocation1",
                "IsEmployee", "IsPreviousEmployee", "CreationDate", "ModificationDate"
            ]
        }
    
        # Assuming apicall.request() returns a JSON-parsed dictionary
        r = apicall.request(api_url, body, "POST")
        
        # Check if the 'TotalPages' field is present and update total_pages
        total_pages = r.get('TotalPages', 1)
    
        for row in r['Records']:

            title_data = row.get('Title')
            title = 'None' if title_data is None else title_data.get('Description')

            address_data = row.get('Address')
            address1 = 'None' if address_data['Address1'] is None else address_data.get('Address1')
            address2 = 'None' if address_data['Address2'] is None else address_data.get('Address2')
            addresstown = 'None' if address_data['Town'] is None else address_data.get('Town')
            addresscounty = 'None' if address_data['County'] is None else address_data.get('County')
            addresscountdesc = 'None' if address_data['Country'] is None else address_data['Country']['Description']
            addresspostcode = 'None' if address_data['PostCode'] is None else address_data.get('PostCode')

            gender_data = row.get('Gender')
            gender = 'None' if gender_data is None else gender_data.get('Description')

            workpermit_data = row.get('WorkPermitType')
            permtype = 'None' if workpermit_data is None else workpermit_data.get('Description')

            location_data = row.get('PreferredLocation1')
            location = 'None' if location_data is None else location_data.get('Description')

            p1 = record(
                row.get("CandidateId"), 
                title,
                row.get("FirstName"), 
                row.get("Surname"), 
                address1,
                address2,
                addresstown,
                addresscounty,
                addresscountdesc,
                addresspostcode, 
                row.get("Telephone"),
                row.get("Mobile"),
                row.get("Email"),
                gender,
                row.get("CriminalRecord"),
                row.get("WorkPermit"),
                permtype,
                location, 
                row.get("IsEmployee"),
                row.get("IsPreviousEmployee"), 
                row.get("CreationDate"),
                row.get("ModificationDate")
            )
    
            sql_query = """INSERT INTO Temp_Candidates (
                        CandidateId, Title, FirstName, Surname, Address1, Address2, 
                        Town, County, Country, PostCode, Telephone, Mobile, Email, 
                        Gender, CriminalRecord, WorkPermit, WorkPermitType, 
                        PreferredLocation1, IsEmployee, IsPreviousEmployee, 
                        CreationDate, ModificationDate
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""
    
            db.query(sql_query, p1)
            db.commit()
        
        # Move to the next page
        current_page += 1

    # Execute a SELECT statement
    results = db.query("SELECT COALESCE( (select CONVERT(NVARCHAR(26), max( C.ModificationDate), 126) + 'Z' FROM Candidates C),  CONVERT(NVARCHAR(26), '2023/01/01T00:00:00Z', 26))as [date]")

    for row in results:
        filterdate = row[0]
        sql_query = "UPDATE table_updaterd SET last_run = ? WHERE table_name = 'Candidates';"

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
