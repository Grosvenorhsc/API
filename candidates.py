import apicall
import sql
from datetime import datetime
import pyodbc
import checkfile
import logging
from dotenv import dotenv_values

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
    # Establish the database connection using environment variables
    cnxn = pyodbc.connect(f"DRIVER={{SQL Server}};SERVER={config['DB_SERVER']};DATABASE={config['DB_NAME']};UID={config['DB_USERNAME']};PWD={config['DB_PASSWORD']}")
    logging.info('Connected to the database')
except Exception as e:
    # Log the error message
    logging.error('Failed to connect to the database: %s', str(e), exc_info=True)
    # Exit or handle the error appropriately

def get_candidates():
    class record:
        def __init__(self, CandidateId, Title, FirstName, Surname, Address1, Address2, Town, County, Country, PostCode, Telephone, Mobile, Email, Gender, CriminalRecord, WorkPermit, WorkPermitType, PreferredLocation1, IsEmployee, IsPreviousEmployee, CreationDate, ModificationDate):
            # Convert all data to string type and store in instance variables
            self.CandidateId = checkfile.validate_parameters(str(CandidateId).lower())
            self.Title = checkfile.validate_parameters(str(Title).lower())
            self.FirstName = checkfile.validate_parameters(str(FirstName).lower())
            self.Surname = checkfile.validate_parameters(str(Surname).lower())
            self.Address1 = checkfile.validate_parameters(str(Address1).lower())
            self.Address2 = checkfile.validate_parameters(str(Address2).lower())
            self.Town = checkfile.validate_parameters(str(Town).lower())
            self.County = checkfile.validate_parameters(str(County).lower())
            self.Country = checkfile.validate_parameters(str(Country).lower())
            self.PostCode = checkfile.validate_parameters(str(PostCode).lower())
            self.Telephone = checkfile.validate_parameters(str(Telephone).lower())
            self.Mobile = checkfile.validate_parameters(str(Mobile).lower())
            self.Email = checkfile.validate_parameters(str(Email).lower())
            self.Gender = checkfile.validate_parameters(str(Gender).lower())
            self.CriminalRecord = checkfile.validate_parameters(str(CriminalRecord).lower())
            self.WorkPermit = checkfile.validate_parameters(str(WorkPermit).lower())
            self.WorkPermitType = checkfile.validate_parameters(str(WorkPermitType).lower())
            self.PreferredLocation1 = checkfile.validate_parameters(str(PreferredLocation1).lower())
            self.IsEmployee = checkfile.validate_parameters(str(IsEmployee).lower())
            self.IsPreviousEmployee = checkfile.validate_parameters(str(IsPreviousEmployee).lower())
            self.CreationDate = str(CreationDate)
            self.ModificationDate = str(ModificationDate)

    api_url = base_url + "candidates/search"

    try:
        # Execute a SELECT statement
        result = cnxn.execute("SELECT COALESCE((SELECT TOP (1) CONVERT(NVARCHAR(26), last_run, 126) + 'Z' FROM table_updaterd WHERE table_name = 'Candidates'), CONVERT(NVARCHAR(26), '2023/01/01T00:00:00Z', 26)) AS [date]")

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
                    "Route": "Candidate.ModificationDate",
                    "Value": str(filterdate).replace("/", "-"),
                    "Operation": "GreaterThan"
                }
            ],
            "ResponseBlocks": [
                "CandidateId",
                "Title",
                "FirstName",
                "Surname",
                "Address",
                "Telephone",
                "Mobile",
                "Email",
                "Gender",
                "CriminalRecord",
                "WorkPermit",
                "WorkPermitType",
                "PreferredLocation1",
                "IsEmployee",
                "IsPreviousEmployee",
                "CreationDate",
                "ModificationDate"
            ]
        }

        paginated = True

        r = apicall.request(api_url, body, paginated)

        for row in r:
            p1 = record(
                str(row.get("CandidateId")),
                str(row.get("Title.Description")),
                str(row.get("FirstName")),
                str(row.get("Surname")),
                str(row.get("Address.Address1")),
                str(row.get("Address.Address2")),
                str(row.get("Address.Town")),
                str(row.get("Address.County")),
                str(row.get("Address.Country.Description")),
                str(row.get("Address.PostCode")),
                str(row.get("Telephone")),
                str(row.get("Mobile")),
                str(row.get("Email")),
                str(row.get("Gender.Description")),
                str(row.get("CriminalRecord")),
                str(row.get("WorkPermit")),
                str(row.get("WorkPermitType.Description")),
                str(row.get("PreferredLocation1.Description")),
                str(row.get("IsEmployee")),
                str(row.get("IsPreviousEmployee")),
                str(row.get("CreationDate")),
                str(row.get("ModificationDate"))
            )

            # Log the company ID
            logging.info('Processed record: CandidateReferenceId=%s', p1.CandidateId)

            sql_query = "INSERT INTO Temp_Candidates (CandidateId, Title, FirstName, Surname, Address1, Address2, Town, County, Country, PostCode, Telephone, Mobile, Email, Gender, CriminalRecord, WorkPermit, WorkPermitType, PreferredLocation1, IsEmployee, IsPreviousEmployee, CreationDate, ModificationDate) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"

            sql.request(p1, sql_query)

            # Log the CandidateId
            logging.info('Processed record: CandidateId=%s', p1.CandidateId)

    except Exception as e:
        # Log the error message
        logging.error('Error occurred: %s', str(e), exc_info=True)
