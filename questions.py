import time
import requests
import tokens
import json
import pandas as pd
import pyodbc
import apicall
import sql
import hashlib
import re
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

# Defining a questions class to store question details
def get_questions():
    class questions:
        def __init__(self, Answer, QuestionId, candidateid, comp_fk):
            # Initializing class properties
            self.Answer = checkfile.validate_parameters(str(Answer))
            self.QuestionId = checkfile.validate_parameters(str(QuestionId).lower())
            self.candidateid = checkfile.validate_parameters(str(candidateid).lower())
            self.comp_fk = checkfile.validate_parameters(str(comp_fk))

    # Retrieving the candidate IDs for which questions need to be retrieved
    result = cnxn.execute("SELECT C.[CandidateId] FROM [Eploy].[dbo].Candidates C join Placements P on C.CandidateId = P.Candidate WHERE P.PlacementStatus = 'offer accepted' or P.Candidate in (select C.CandidateId from Candidates C where C.CandidateId not in (SELECT Q.candidateid FROM Questions Q))")
    rows = result.fetchall()

    # Looping through the result set
    for row in rows:
        candidateid = row[0]

        # Constructing the API URL to retrieve candidate questions
        base_url = "https://grosvenorhsc.eploy.net/api/"
        api_url = base_url + "candidates/" + str(candidateid) + "/questions"
       
        # Making the API call to retrieve candidate questions
        paginated = False
        element = "questions"
        r = apicall.request(api_url, element, paginated)

        # Inserting the candidate question details into the database
        if isinstance(r[0], pd.Series):
            for record in r:

                # Create an instance of the MD5 hash object
                hash_obj = hashlib.md5()

                result = str(record.get("QuestionId")) + str(candidateid)

                # Update the hash object with the string to be hashed
                hash_obj.update(result.encode())

                # Get the hexadecimal representation of the hash
                comp_fk = hash_obj.hexdigest()

                # Creating a questions object to store question details
                if record.get("AnswerType") == 'Date' or record.get("AnswerType") == 'Boolean':
                    p1 = questions(
                        str(record.get("Answer")),
                        str(record.get("QuestionId")),
                        str(candidateid),
                        str(comp_fk),
                    )
                else:
                    p1 = questions(
                        str(record.get("Answer.Description")),
                        str(record.get("QuestionId")),
                        str(candidateid),
                        str(comp_fk),
                    )

                questionids = [
                    30,#Date of Birth:
                    122,#Did one of our employees recommend you for this role?
                    202,#What is your sexual orientation?
                    201,#What is your gender identity?
                    204,#What is your ethnic group?
                    226,#What is your religion?
                    228,#Do you identify as trans?
                    251,#What is your nationality
                    252,#Are you male or female
                    253,#Do you have the right to work in the UK?
                    257,#Do you have a full driving licence?
                    258,#Do you have access to a vehicle to use for work?
                    260,#Would you be happy to work alternate weekends?
                    261,#It is a Domiciliary care role that you are applying for? This would involve providing care to vulnerable people within their own homes and providing care such as intimate personal bathing and caring for both genders. Are you happy to do this?
                    262,#Do you have any of the below to evidence entitlement to work in the UK? - Valid UK Passport, - Expired UK Passport, - UK Birth Certificate (and proof of NI), - Current Biometric Residence Permit (front and back), - EU Settlement Letter and Share Code, - Application Registration Card (ARC) front and back
                    270,#Do you have a fully enhanced adult and child DBS disclosure that you pay yearly to be subscribed to?
                    271,#Shifts include Morning/Lunch 7am-2pm Tea and beds 3pm-10pm. Could you work these shifts?
                    274,#Training Stage
                    276,#DBS Stage
                    277,#Training Sent:
                    278,#Training Completed
                    280,#DBS Sent
                    281,#DBS Returned
                    282,#DBS Number
                    285,#POVA Stage
                    286,#POVA Sent
                    287,#POVA Returned
                    289,#File Issued
                    290,#ID Badge
                    291,#Coldharbour Reference
                    294,#Received References Sufficient
                    295,#International Candidate
                    306,#CH Addition Date
                    307,#Interview Date
                    308,#International Sponsorship
                    310,#first ref sent
                    311,#all refs recived
                ]
                
                questionid = int(record.get("QuestionId"))

                if questionid in questionids:    

                    # Log the company ID
                    logging.info('Processed record: QuestionId=%s, CandidateId=%s', p1.QuestionId, p1.candidateid)

                    # Constructing the SQL query to insert question details into the database
                    sql_query = "INSERT INTO Temp_Questions (Answer,QuestionId,candidateid,comp_fk) VALUES (?,?,?,?);"

                    # Executing the SQL query to insert the question details
                    sql.request(p1, sql_query)          
               
        else:
            print('error')
            return