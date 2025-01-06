import apicall
import sql
import hashlib
import database_utils

# Defining a questions class to store question details
def fixbroken():
    
    db = database_utils.Database()
    db.connect()
    
    class questions:
        def __init__(self, Answer, Title, QuestionId, candidateid, comp_fk):
            # Initializing class properties
            self.Answer = Answer
            self.Title = Title
            self.QuestionId = QuestionId
            self.candidateid = candidateid
            self.comp_fk = comp_fk

    # Retrieving the candidate IDs for which questions need to be retrieved
    result = db.query("SELECT [Candidate] FROM [Eploy].[dbo].[Placements] P WHERE P.PlacementStatus in('Contract Reviewed', 'Your Contract')")

    # Looping through the result set
    for candidate in result:
        candidateid = candidate[0]

        # Constructing the API URL to retrieve candidate questions
        base_url = "https://grosvenorhsc.eploy.net/api/"
        api_url = base_url + "candidates/" + str(candidateid) + "/questions"
       
        # Making the API call to retrieve candidate questions
        body = None
        # Call the API to retrieve the company data
        r = apicall.request(api_url, body, "GET")

        # Loop through each record in the response and insert into the SQL Server database
        #try:
        for question in r:

            # Create an instance of the MD5 hash object
            hash_obj = hashlib.md5()

            result = str(question.get("QuestionId")) + str(candidateid)

            # Update the hash object with the string to be hashed
            hash_obj.update(result.encode())

            # Get the hexadecimal representation of the hash
            comp_fk = hash_obj.hexdigest()

            # Creating a questions object to store question details
            if question.get("AnswerType") == 'Date' or question.get("AnswerType") == 'Boolean':
                p1 = questions(
                    str(question.get("Answer"))[:50],
                    str(question.get("Title"))[:50],
                    str(question.get("QuestionId")),
                    str(candidateid),
                    str(comp_fk),
                )
            else:

                Answer_data = question.get('Answer')
                Answer = 'None' 
                if Answer_data is not None and Answer_data != '' and isinstance(Answer_data, dict):
                    Answer = Answer_data.get('Description', 'None')

                p1 = questions(
                    Answer[:50],
                    str(question.get("Title"))[:50],
                    str(question.get("QuestionId")),
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
                312,#Application Processed Date
                313,#Application Date
            ]
            
            questionid = int(question.get("QuestionId"))

            if questionid in questionids:    
                print("processing question "+str(questionid))
                # Constructing the SQL query to insert question details into the database
                sql_query = "INSERT INTO Temp_Questions (Answer, Title, QuestionId, candidateid,comp_fk) VALUES (?,?,?,?,?);"

                db.query(sql_query, p1)
                db.commit()
            else:
                print("question not needed")
 
        # except Exception as e:
        #     print(f"An unexpected error occurred: {str(e)}")
    db.close()