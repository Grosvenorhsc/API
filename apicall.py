import time                 # Import the time module
import requests             # Import the requests library for making HTTP requests
import tokens               # Import the tokens module
#import json                 # Import the JSON module for working with JSON data
import pandas as pd         # Import the pandas library for data manipulation and analysis
#import sys                  # Import the sys module for system-specific parameters and functions
#from dotenv import dotenv_values  # Import the dotenv_values function from python-dotenv
import RateLimiter


# max_attempts = 4
# retry_statuses = [408, 429, 500, 502, 503, 504, 505, 507, 508, 509, 510]

def request(api_url, body, requesttype):
    # Check if the bearer token has expired or is about to expire, and get a new one if needed
    tokens.check_bearer_token()

    # Set the Authorization header to include the bearer token
    headers = {
        "Authorization": "Bearer " + tokens.bt.access_token
    }
                    
    RateLimiter.rate_limiter_per_day()
    if requesttype == 'GET':
        return_data = requests.get(api_url, headers=headers)
    elif requesttype == 'POST':                   
        return_data = requests.post(api_url, json=body, headers=headers)
    time.sleep(0.1) 

    # Parse the response JSON
    r = return_data.json()

    # records = []

    # flat_dataframe = pd.json_normalize(r)

    # for index, row in flat_dataframe.iterrows():
    #     record = row
    #     records.append(record)
    
    return r

  