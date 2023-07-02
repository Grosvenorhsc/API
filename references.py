import pandas as pd
import pyodbc
import apicall
import sql
import logging
from dotenv import dotenv_values
import checkfile

# Load environment variables from .env file
config = dotenv_values('.env')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(filename)s - %(message)s',
    filename='project.log'
)

# Establishing a connection to the SQL Server
try:
    # Establish the database connection using environment variables
    cnxn = pyodbc.connect(f"DRIVER={{SQL Server}};SERVER={config['DB_SERVER']};DATABASE={config['DB_NAME']};UID={config['DB_USERNAME']};PWD={config['DB_PASSWORD']}")
    logging.info('Connected to the database')
except Exception as e:
    # Log the error message
    logging.error('Failed to connect to the database: %s', str(e), exc_info=True)
    # Exit or handle the error appropriately

# Defining a reference class to store reference details
def get_refference():
    class refference:
        def __init__(self, CandidateReferenceId, CandidateReferenceType, Referee, Company, Relationship, ReasonForLeaving, CreationDate, ModificationDate, candidateid):
            # Initializing class properties
            self.CandidateReferenceId = checkfile.validate_parameters(str(CandidateReferenceId).lower())
            self.CandidateReferenceType = checkfile.validate_parameters(str(CandidateReferenceType).lower())
            self.Referee = checkfile.validate_parameters(str(Referee).lower())
            self.Company = checkfile.validate_parameters(str(Company).lower())
            self.Relationship = checkfile.validate_parameters(str(Relationship).lower())
            self.ReasonForLeaving = checkfile.validate_parameters(str(ReasonForLeaving).lower())
            self.CreationDate = checkfile.validate_parameters(str(CreationDate))
            self.ModificationDate = str(ModificationDate)
            self.candidateid = str(candidateid).lower()

    # Retrieving the candidate IDs for which references need to be retrieved
    result = cnxn.execute("SELECT [Candidate] FROM [Eploy].[dbo].[Placements] WHERE PlacementStatus = 'offer accepted'")
    rows = result.fetchall()

    # Looping through the result set
    for row in rows:
        candidateid = row[0]

        # Constructing the API URL to retrieve candidate references
        base_url = "https://grosvenorhsc.eploy.net/api/"
        api_url = base_url + "candidates/" + str(candidateid) + "/references"

        # Making the API call to retrieve candidate references
        paginated = False
        element = "References"
        r = apicall.request(api_url, element, paginated)

        # Inserting the candidate reference details into the database
        if isinstance(r[0], pd.Series):
            for record in r:

                # Creating a reference object to store reference details
                p1 = refference(
                    str(record.get("CandidateReferenceId")),
                    str(record.get("CandidateReferenceType.Description")),
                    str(record.get("Referee")),
                    str(record.get("Company")),
                    str(record.get("Relationship")),
                    str(record.get("ReasonForLeaving")),
                    str(record.get("CreationDate")),
                    str(record.get("ModificationDate")),
                    str(candidateid)
                )

                # Log the company ID
                logging.info('Processed record: CandidateReferenceId=%s', p1.CandidateReferenceId)

                # Constructing the SQL query to insert reference details into the database
                sql_query = "INSERT INTO Temp_Refference (CandidateReferenceId,CandidateReferenceType,Referee,Company,Relationship,ReasonForLeaving,CreationDate,ModificationDate,candidateid) VALUES (?,?,?,?,?,?,?,?,?);"

                # Executing the SQL query to insert the reference details
                sql.request(p1, sql_query)
        else:
            print('error')