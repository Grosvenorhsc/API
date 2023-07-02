import apicall
import sql
from datetime import datetime
import pyodbc

base_url = "https://grosvenorhsc.eploy.net/api/"

api_url = base_url + "candidates/9824/questions"

 # Making the API call to retrieve candidate questions
paginated = False
element = "questions"
r = apicall.request(api_url, element, paginated)

print(r)