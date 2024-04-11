from datetime import datetime
import apicall
import database_utils
    
# Defining a reference class to store reference details
def get_refference():
    
    db = database_utils.Database()
    db.connect()

    class refference:
        def __init__(self, candidateid, CandidateReferenceId, CandidateReferenceType, Referee, Company, Relationship, ReasonForLeaving, CreationDate, ModificationDate):
            # Initializing class properties
            self.candidateid = candidateid
            self.CandidateReferenceId = CandidateReferenceId
            self.CandidateReferenceType = CandidateReferenceType
            self.Referee = Referee[:50]
            self.Company = 'None' if Company is None else Company[:50]
            self.Relationship = 'None' if Relationship is None else Relationship[:50]
            self.ReasonForLeaving = 'None' if ReasonForLeaving is None else ReasonForLeaving[:50]
            self.CreationDate = CreationDate
            self.ModificationDate = ModificationDate
            

    # Retrieving the candidate IDs for which references need to be retrieved
    result = db.query("SELECT [Candidate] FROM [Eploy].[dbo].[Applications] WHERE concat([Stage],' - ',[Status]) in ('DBS Check - To Be Completed','Offers & Placements - Final Checks Failed - ID','Offers & Placements - Offer Accepted','Offers & Placements - Onboarding Checked - Candidate Ready (Coldharbour)','Offers & Placements - Contract Reviewed', 'Offers & Placements - Your Contract', 'Offers & Placements - Contract Accepted')")
    
    # Looping through the result set
    for candidate in result:
        candidateid = candidate[0]

        # Constructing the API URL to retrieve candidate references
        base_url = "https://grosvenorhsc.eploy.net/api/"
        api_url = base_url + "candidates/" + str(candidateid) + "/references"

        body = None
        # Call the API to retrieve the company data
        r = apicall.request(api_url, body, "GET")

        # Loop through each record in the response and insert into the SQL Server database
        try:
            for row in r['References']:

                CandidateReferenceType_data = row.get('CandidateReferenceType')
                CandidateReferenceType = 'None' if CandidateReferenceType_data is None else CandidateReferenceType_data.get('Description')

                # Creating a reference object to store reference details
                p1 = refference(
                    candidateid,
                    row.get("CandidateReferenceId"),
                    CandidateReferenceType,
                    row.get("Referee"),
                    row.get("Company"),
                    row.get("Relationship"),
                    row.get("ReasonForLeaving"),
                    row.get("CreationDate"),
                    row.get("ModificationDate")
                    
                )

                # Constructing the SQL query to insert reference details into the database
                sql_query = "INSERT INTO Temp_Refference (CandidateReferenceId,CandidateReferenceType,Referee,Company,Relationship,ReasonForLeaving,CreationDate,ModificationDate,candidateid) VALUES (?,?,?,?,?,?,?,?,?);"

                db.query(sql_query, p1)
                db.commit()
 
        except Exception as e:

            if isinstance(e, dict) and 'error_message' in e and e['error_message'] == 'No record could be found for the requested URI':
                print("No record could be found for the requested URI")
            else:
                print(f"An unexpected error occurred: {str(e)}")
    db.close()
