import requests
from datetime import datetime, timedelta
import time
from dotenv import load_dotenv, find_dotenv
import os
import RateLimiter

# Find and load the .env file
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

base_url = "https://grosvenorhsc.eploy.net/api/"

# create a class to hold the bearer token and its metadata
class bearertoken:
    access_token = ""
    expires_in = ""
    token_type = ""
    scope = ""
    expire_time = datetime.now()

# create an instance of the bearertoken class
bt = bearertoken()

# function to retrieve a new bearer token from the API
def get_bearer_token():
    api_url = base_url + "token"

    # create the request body with client credentials and requested scopes
    body = {
        "grant_type": "client_credentials",
        # "client_id": "QHluVeJPlVyiKaUHwLzx",
        # "client_secret": "sJAErSMHSAtztvRqEVWh",
        "client_id": os.getenv("CLIENT_ID"),
        "client_secret": os.getenv("CLIENT_SECRET"),
        "scope": "actions.read,applications.read,candidates.read,candidates.update,contacts.read,payrates.read,paysalaries.read,placements.read,vacancies.read,vacancytemplates.read,companies.read"
    }
    
    RateLimiter.rate_limiter_per_day()
    # make the request to the API and get the response
    return_data = requests.post(api_url, data=body)
    time.sleep(0.1) 

    # parse the response JSON and update the bearertoken instance variables
    r = return_data.json()
    bt.access_token = r["access_token"]
    bt.expires_in = r["expires_in"]
    bt.token_type = r["token_type"]
    bt.scope = r["scope"]

    # update the token expiration time based on the current time and the expiration time in the response
    bt.expire_time = bt.expire_time + timedelta(0, int(r["expires_in"]))

# function to check if the bearer token is expired and get a new one if needed
def check_bearer_token():
    # check if the token has already expired or is about to expire
    if bt.expire_time <= datetime.now() + timedelta(seconds=20):
        # if the token is expired or about to expire, get a new one
        get_bearer_token()
