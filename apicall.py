import time
import requests
import tokens
import json
import pandas as pd
import sys
import logging
from dotenv import dotenv_values

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(filename)s - %(message)s',
    handlers=[logging.FileHandler('project.log')]  # Specify the file handler for logging to "project.log"
)

# Load environment variables from .env file
config = dotenv_values('.env')

max_attempts=config["MAX_RETRY_ATTEMPTS"]
retry_statuses = [408, 429, 500, 502, 503, 504, 505, 507, 508, 509, 510]

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(filename)s - %(message)s',
    filename='project.log'
)

def request(api_url, body, paginated):
    # check if the bearer token has expired or is about to expire, and get a new one if needed
    tokens.check_bearer_token()

    # set the Authorization header to include the bearer token
    headers = {
        "Authorization": "Bearer " + tokens.bt.access_token
    }

    records = []

    if paginated:
        keep_looping = True
        first_loop = True
        num_pages = ""
        current_page = 1

        while keep_looping:
            if first_loop:
                attempts = 0
                try:
                    while attempts < int(max_attempts):
                        # make the first API request to get the total number of pages and the first page of results
                        return_data = requests.post(api_url, json=body, headers=headers)

                        # parse the response JSON
                        r = return_data.json()
                        status_code = return_data.status_code
                    
                        if status_code == 404:
                            records.append('error')
                            logging.error("Error in paginated API request. Status Code: 404")
                            break
                        elif status_code == 200:
                            # get the current page number and the total number of pages
                            if "CurrentPage" in r:
                                current_page = r["CurrentPage"]
                                num_pages = r["TotalPages"]
                            else:
                                current_page = 1
                                num_pages = 1

                            # Use pandas to flatten the nested dictionary into a dataframe
                            flat_dataframe = pd.json_normalize(r["Records"])

                            # loop through the flattened dataframe and add each row as a record to the records list
                            for index, row in flat_dataframe.iterrows():
                                record = row
                                records.append(record)

                            first_loop = False

                            # check if we've reached the last page of results
                            if current_page == num_pages:
                                keep_looping = False
                                logging.info("Successfully fetched all paginated records")
                            break
                        elif status_code in retry_statuses:
                            
                            attempts += 1
                            if attempts < max_attempts:
                                # Wait for some time before retrying
                                logging.info("Retrying API request. Attempt: %d", attempts)  # Log the retry attempt
                                time.sleep(1)
                                continue
                            else:
                                # Run your code here for exceeding maximum attempts
                                
                                records.append('error')
                                logging.error("Maximum attempts reached. Request failed.")  # Log the maximum attempts reached
                                break

                except requests.exceptions.RequestException as e:
                    logging.error("Error in paginated API request: %s", str(e), exc_info=True)
                    records.append('error')
                    break
            else:
                try:
                    attempts = 0
                    while attempts < int(max_attempts):
                        # make subsequent API requests to get the next page of results
                        body["Paging"]["RequestedPage"] = current_page + 1

                        return_data = requests.post(api_url, json=body, headers=headers)

                        r = return_data.json()
                        status_code = return_data.status_code
                        
                        if status_code == 404:
                            records.append('error')
                            logging.error("Error in paginated API request. Status Code: 404")
                            break
                        elif status_code == 200:

                            current_page = r["CurrentPage"]

                            flat_dataframe = pd.json_normalize(r["Records"])


                            for index, row in flat_dataframe.iterrows():
                                record = row
                                records.append(record)

                            # check if we've reached the last page of results
                            if current_page == num_pages:
                                keep_looping = False
                                logging.info("Successfully fetched all paginated records")

                            # Pause for 0.1 seconds between API calls
                            time.sleep(0.1)
                            break
                        elif status_code in retry_statuses:
                            attempts += 1
                            if attempts < max_attempts:
                                # Wait for some time before retrying
                                logging.info("Retrying API request. Attempt: %d", attempts)  # Log the retry attempt
                                time.sleep(1)
                                continue
                            else:
                                # Run your code here for exceeding maximum attempts
                                
                                records.append('error')
                                logging.error("Maximum attempts reached. Request failed.")  # Log the maximum attempts reached
                                break
                except requests.exceptions.RequestException as e:
                    logging.error("Error in paginated API request: %s", str(e), exc_info=True)
                    records.append('error')
                    break
    else:
        try:
            attempts = 0
            while attempts < int(max_attempts):
                # make a non-paginated API request
                tokens.check_bearer_token()
                return_data = requests.get(api_url, headers=headers)

                # Pause for 0.1 seconds between API calls
                time.sleep(0.1)

                r = return_data.json()
                status_code = return_data.status_code

                if status_code == 404:
                    records.append('error')
                    logging.error("Error in non-paginated API request. Status Code: 404")
                    break
                elif status_code == 200:
                    if body == 'References':
                        # Use pandas to flatten the nested dictionary into a dataframe
                        flat_dataframe = pd.json_normalize(r[body])
                        for index, row in flat_dataframe.iterrows():
                            record = row
                            records.append(record)
                    elif body == 'questions':
                        # loop through each question in the response and flatten it into a record
                        for question in r:
                            flat_dataframe = pd.json_normalize(question)
                            for index, row in flat_dataframe.iterrows():
                                record = row
                                records.append(record)
                    else:
                        records.append('error')
                    break
                elif status_code in retry_statuses:
                    attempts += 1
                    if attempts < max_attempts - 1:
                        # Wait for some time before retrying
                        logging.info("Retrying API request. Attempt: %d", attempts)  # Log the retry attempt
                        time.sleep(1)
                        continue
                    else:
                        # Run your code here for exceeding maximum attempts
                        logging.error("Maximum attempts reached. Request failed.")  # Log the maximum attempts reached
                        break
        except requests.exceptions.RequestException as e:
            logging.error("Error in non-paginated API request: %s", str(e), exc_info=True)
            records.append('error')

    return records
