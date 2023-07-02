main.py Documentation
This documentation provides an overview of the "main.py" script, which imports various modules and performs specific tasks related to candidate data management. The script includes importing modules, configuring logging, importing necessary data, and logging the start and end time of the run.

Module Imports
The following modules are imported at the beginning of the script:

candidates: This module contains functions related to managing candidate data.
placements: This module provides functions for managing placement data.
applications: This module handles application-related operations.
companies: This module includes functions for managing company data.
references: This module provides functions for handling reference data.
questions: This module contains functions related to managing questions.
vacancys: This module handles vacancy-related operations.
actions: This module provides functions for managing actions.
Workflow: This module includes functions related to workflow management.
applications_status_history: This module handles application status history data.
logging: This module is part of the Python standard library and is used for logging purposes.
datetime: This module is part of the Python standard library and is used for working with dates and times.
logging.handlers: This module is part of the Python standard library and provides additional logging handlers.
os: This module is part of the Python standard library and provides functions for interacting with the operating system.
Logging Configuration
The script configures logging with the following settings:

Log formatter: The log messages will include the timestamp, log level, and log message.
Log file: A log file named "project.log" is created in the current working directory.
Rotating file handler: A rotating file handler is created with a maximum file size of 10 MB and a backup count of 5. This ensures that the log file is rotated when it reaches the maximum size, and up to 5 backup files are kept.
Logger: A logger named __name__ is created with the log level set to INFO. The log handler is added to the logger.
Run Start Time
The script records the start time of the run using the datetime.datetime.now() function and logs it using the logger. The start time is important for measuring the duration of the script execution.

Importing Necessary Data
The script imports necessary data from various modules. The following functions are called to retrieve the data:

companies.get_companies(): Imports company data.
vacancys.get_vacancys(): Imports vacancy data.
candidates.get_candidates(): Imports candidate data.
questions.get_questions(): Imports question data.
references.get_refference(): Imports reference data.
applications.get_applications(): Imports application data.
placements.get_placements(): Imports placement data.
applications_status_history.get_status_history(): Imports application status history data.
Run End Time and Duration
After importing the necessary data, the script records the end time of the run using the datetime.datetime.now() function and logs it using the logger. The duration of the run is calculated by subtracting the start time from the end time.

Log File Size Check and Rotation
The script checks if the log file has reached its maximum size (log_handler.maxBytes). If the maximum size is exceeded, the following actions are performed:

The log file is renamed to an archive file with a timestamp appended to the filename.
A new log file is created, replacing the previous log file.
This log file rotation ensures that the log files do not grow too large and maintains a limited number of backup log files.


token.py Documentation
This documentation provides an overview of the "token.py" script, which imports various modules and defines functions for managing bearer tokens used for authentication. The script includes module imports, logging configuration, bearer token management, and a test code snippet.

Module Imports
The following modules are imported at the beginning of the script:

requests: This module is used for making HTTP requests to the API.
datetime: This module is part of the Python standard library and is used for working with dates and times.
logging: This module is part of the Python standard library and is used for logging purposes.
dotenv.dotenv_values: This module is used for loading environment variables from a .env file.
time: This module is part of the Python standard library and is used for time-related operations.
os: This module is part of the Python standard library and provides functions for interacting with the operating system.
Environment Variables
The script loads environment variables from a .env file using the dotenv_values() function from the dotenv module. The environment variables are stored in the config dictionary.

Logging Configuration
The script configures logging with the following settings:

Log level: The log level is set to INFO.
Log format: The log messages include the timestamp, log level, filename, and log message.
Log file: The log messages are written to a file named "project.log" in the current working directory.
Bearer Token Management
The script defines a bearertoken class to hold the bearer token and its metadata. An instance of this class named bt is created.

The script includes the following functions for managing bearer tokens:

get_bearer_token(): This function retrieves a new bearer token from the API by making a request with client credentials and requested scopes. The response is parsed, and the bearertoken instance variables are updated accordingly.
check_bearer_token(): This function checks if the bearer token has expired or is about to expire. If the token is expired or about to expire, it calls the get_bearer_token() function to obtain a new token.
Test Code
The script includes a test code snippet that logs a message indicating the start of the script execution. This code serves as an example and can be modified or removed as needed.

sql.py Documentation
This documentation provides an overview of the "sql.py" script, which imports various modules and defines functions for working with a SQL Server database. The script includes module imports, logging configuration, database connection establishment, and a function for executing parameterized queries.

Module Imports
The following modules are imported at the beginning of the script:

pyodbc: This module is used for connecting to a SQL Server database and executing SQL queries.
re: This module is part of the Python standard library and is used for working with regular expressions.
time: This module is part of the Python standard library and is used for time-related operations.
logging: This module is part of the Python standard library and is used for logging purposes.
dotenv.dotenv_values: This module is used for loading environment variables from a .env file.
Environment Variables
The script loads environment variables from a .env file using the dotenv_values() function from the dotenv module. The environment variables are stored in the config dictionary.

Logging Configuration
The script configures logging with the following settings:

Log level: The log level is set to INFO.
Log format: The log messages include the timestamp, log level, filename, and log message.
Log file: The log messages are written to a file named "project.log" in the current working directory.
Database Connection Establishment
The script defines a connect_to_database() function to establish a connection to the SQL Server database using the pyodbc.connect() function. The function uses the database server, name, username, and password retrieved from the config dictionary.

Parameterized Query Execution
The script defines a request() function for executing a parameterized query to insert records into the database. The function takes the record object, the SQL query, and optional parameters for maximum retries and retry delay.

Within the function, the record object's properties are processed to convert empty strings to NULL and check for values matching the regex pattern for NaN or None. The parameterized query is then executed with the list of parameters using the cnxn.cursor().execute() method.

If a deadlock error is encountered during query execution, the function retries a maximum number of times with a specified delay. Other errors are logged, and the function exits the loop.

Usage Example
The script includes code to establish a database connection and define the request() function. However, it does not provide an example of calling the request() function with a specific SQL query and record object. You would need to modify the script or import it into another module to use the request() function with your own SQL queries and record objects.

apicall.py Documentation
This documentation provides an overview of the "apicall.py" script, which imports various modules and defines a function for making HTTP requests to an API and handling paginated responses. The script includes module imports, logging configuration, and the request() function for making API requests.

Module Imports
The following modules are imported at the beginning of the script:

time: This module is part of the Python standard library and is used for time-related operations.
requests: This module is used for making HTTP requests.
tokens: This module is a custom module for managing bearer tokens.
json: This module is part of the Python standard library and is used for working with JSON data.
pandas: This module provides data manipulation and analysis tools.
sys: This module is part of the Python standard library and provides system-specific parameters and functions.
logging: This module is part of the Python standard library and is used for logging messages.
dotenv.dotenv_values: This module is used for loading environment variables from a .env file.
Logging Configuration
The script configures logging with the following settings:

Log level: The log level is set to INFO.
Log format: The log messages include the timestamp, log level, filename, and log message.
Log file: The log messages are written to a file named "project.log" in the current working directory.
request() Function
The script defines a request() function that handles making API requests. The function takes parameters for the API URL, request body, and whether the response is paginated.

Within the function, the bearer token is checked for expiration and renewed if needed. The Authorization header is set with the bearer token.

If the response is paginated, the function makes subsequent requests to retrieve all pages of results. It handles potential errors, retries, and pauses between API calls. The results are stored in a list called records.

If the response is not paginated, a non-paginated API request is made, and the response is processed accordingly.

The function returns the records list containing the retrieved data.

Usage Example
The script defines the request() function for making API requests and handling paginated responses. However, it does not provide an example of calling the function with specific API URLs, request bodies, or pagination settings. You would need to modify the script or import it into another module to use the request() function with your own API requests.

vacancys.py Documentation
This documentation provides an overview of the "vacancys.py" script, which imports various modules and defines functions for retrieving vacancy data from an API and storing it in a SQL Server database. The script includes module imports, logging configuration, database connection establishment, and the get_vacancys() function for retrieving and processing vacancy data.

Module Imports
The following modules are imported at the beginning of the script:

apicall: This module provides the request() function for making API requests.
sql: This module provides functions for executing SQL queries and interacting with a SQL Server database.
pyodbc: This module is used for connecting to a SQL Server database and executing SQL queries.
datetime: This module is part of the Python standard library and is used for working with dates and times.
dateutil.parser: This module is used for parsing dates from strings.
dotenv.dotenv_values: This module is used for loading environment variables from a .env file.
checkfile: This module provides the validate_parameters() function for validating and formatting parameters.
logging: This module is part of the Python standard library and is used for logging messages.
os: This module is part of the Python standard library and provides functions for interacting with the operating system.
Logging Configuration
The script configures logging with the following settings:

Log level: The log level is set to INFO.
Log format: The log messages include the timestamp, log level, filename, and log message.
Log file: The log messages are written to a file named "project.log" in the current working directory.
Database Connection Establishment
The script connects to a SQL Server database using the pyodbc.connect() function. The connection string is constructed using the environment variables retrieved from the .env file.

get_vacancys() Function
The script defines a get_vacancys() function for retrieving vacancy data from the API and storing it in the database. The function uses the following steps:

Executes a SELECT statement to retrieve the last run date from the table_updaterd table.
Constructs the API URL and request body for the vacancies search.
Makes an API request to retrieve the paginated vacancy data.
Iterates through the retrieved data and processes each record.
Constructs a record object and inserts it into the Temp_Vacancys table using an SQL INSERT statement.
Logs the processed record's VacancyId.
Usage Example
The script defines the get_vacancys() function for retrieving and processing vacancy data. However, it does not provide an example of calling the function or how to execute the script as a standalone program. You would need to modify the script or import it into another module to use the get_vacancys() function in your own application.

references.py Documentation
This documentation provides an overview of the "references.py" script, which imports various modules and defines functions for retrieving candidate reference data from an API and storing it in a SQL Server database. The script includes module imports, logging configuration, database connection establishment, and the get_refference() function for retrieving and processing candidate reference data.

Module Imports
The following modules are imported at the beginning of the script:

pandas: This module provides data manipulation and analysis tools.
pyodbc: This module is used for connecting to a SQL Server database and executing SQL queries.
apicall: This module provides the request() function for making API requests.
sql: This module provides functions for executing SQL queries and interacting with a SQL Server database.
logging: This module is part of the Python standard library and is used for logging messages.
dotenv.dotenv_values: This module is used for loading environment variables from a .env file.
checkfile: This module provides the validate_parameters() function for validating and formatting parameters.
Logging Configuration
The script configures logging with the following settings:

Log level: The log level is set to INFO.
Log format: The log messages include the timestamp, log level, filename, and log message.
Log file: The log messages are written to a file named "project.log" in the current working directory.
Database Connection Establishment
The script connects to a SQL Server database using the pyodbc.connect() function. The connection string is constructed using the environment variables retrieved from the .env file.

get_refference() Function
The script defines a get_refference() function for retrieving candidate reference data from the API and storing it in the database. The function uses the following steps:

Executes a SELECT statement to retrieve the candidate IDs for which references need to be retrieved.
Constructs the API URL to retrieve candidate references based on the candidate IDs.
Makes an API request to retrieve the candidate references.
Iterates through the retrieved data and processes each record.
Constructs a refference object to store reference details and inserts it into the Temp_Refference table using an SQL INSERT statement.
Logs the processed record's CandidateReferenceId.
Usage Example
The script defines the get_refference() function for retrieving and processing candidate reference data. However, it does not provide an example of calling the function or how to execute the script as a standalone program. You would need to modify the script or import it into another module to use the get_refference() function in your own application.


questions.py Documentation
This documentation provides an overview of the "questions.py" script, which imports various modules and defines functions for retrieving candidate question data from an API and storing it in a SQL Server database. The script includes module imports, logging configuration, database connection establishment, and the get_questions() function for retrieving and processing candidate question data.

Module Imports
The following modules are imported at the beginning of the script:

time: This module provides functions for working with time-related operations.
requests: This module is used for making HTTP requests to the API.
tokens: This module provides functions for managing bearer tokens.
json: This module is used for working with JSON data.
pandas as pd: This module provides data manipulation and analysis tools.
pyodbc: This module is used for connecting to a SQL Server database and executing SQL queries.
apicall: This module provides the request() function for making API requests.
sql: This module provides functions for executing SQL queries and interacting with a SQL Server database.
hashlib: This module is used for generating hash values.
re: This module provides regular expression matching operations.
logging: This module is part of the Python standard library and is used for logging messages.
dotenv.dotenv_values: This module is used for loading environment variables from a .env file.
checkfile: This module provides the validate_parameters() function for validating and formatting parameters.
Logging Configuration
The script configures logging with the following settings:

Log level: The log level is set to INFO.
Log format: The log messages include the timestamp, log level, filename, and log message.
Log file: The log messages are written to a file named "project.log" in the current working directory.
Database Connection Establishment
The script connects to a SQL Server database using the pyodbc.connect() function. The connection string is constructed using the environment variables retrieved from the .env file.

get_questions() Function
The script defines a get_questions() function for retrieving candidate question data from the API and storing it in the database. The function uses the following steps:

Executes a SELECT statement to retrieve the candidate IDs for which questions need to be retrieved.
Constructs the API URL to retrieve candidate questions based on the candidate IDs.
Makes an API request to retrieve the candidate questions.
Iterates through the retrieved data and processes each record.
Generates a unique hash value for each record using the hashlib module.
Constructs a questions object to store question details and inserts it into the Temp_Questions table using an SQL INSERT statement.
Logs the processed record's QuestionId and CandidateId.
Usage Example
The script defines the get_questions() function for retrieving and processing candidate question data. However, it does not provide an example of calling the function or how to execute the script as a standalone program. You would need to modify the script or import it into another module to use the get_questions() function in your own application.

placement.py Documentation
This documentation provides an overview of the "placement.py" script, which imports various modules and defines a function for retrieving and storing placement data from an API into a SQL Server database. The script includes module imports, logging configuration, database connection establishment, and the get_placements() function for retrieving and processing placement data.

Module Imports
The following modules are imported at the beginning of the script:

sql: This module provides functions for executing SQL queries and interacting with a SQL Server database.
datetime: This module supplies classes for working with dates and times.
pyodbc: This module is used for connecting to a SQL Server database and executing SQL queries.
dotenv.dotenv_values: This module is used for loading environment variables from a .env file.
logging: This module is part of the Python standard library and is used for logging messages.
checkfile: This module provides the validate_parameters() function for validating and formatting parameters.
Logging Configuration
The script configures logging with the following settings:

Log level: The log level is set to INFO.
Log format: The log messages include the timestamp, log level, filename, and log message.
Log file: The log messages are written to a file named "project.log" in the current working directory.
Database Connection Establishment
The script connects to a SQL Server database using the pyodbc.connect() function. The connection string is constructed using the environment variables retrieved from the .env file.

get_placements() Function
The script defines a get_placements() function for retrieving placement data from the API and storing it in the database. The function uses the following steps:

Executes a SELECT statement to retrieve the filter date for filtering placements.
Constructs the API URL to retrieve placement data based on the filter date.
Makes an API request to retrieve the placement data.
Iterates through the retrieved data and processes each record.
Creates a record object to store placement details and inserts it into the Temp_Placements table using an SQL INSERT statement.
Logs the processed record's PlacementId.
Usage Example
The script defines the get_placements() function for retrieving and processing placement data. However, it does not provide an example of calling the function or how to execute the script as a standalone program. You would need to modify the script or import it into another module to use the get_placements() function in your own application.

companies.py Documentation
This documentation provides an overview of the "companies.py" script, which imports various modules and defines a function for retrieving and storing company data from an API into a SQL Server database. The script includes module imports, logging configuration, database connection establishment, and the get_companies() function for retrieving and processing company data.

Module Imports
The following modules are imported at the beginning of the script:

sql: This module provides functions for executing SQL queries and interacting with a SQL Server database.
pyodbc: This module is used for connecting to a SQL Server database and executing SQL queries.
datetime: This module supplies classes for working with dates and times.
dateutil.parser: This module provides a parser for parsing dates from string representations.
dotenv.dotenv_values: This module is used for loading environment variables from a .env file.
checkfile: This module provides the validate_parameters() function for validating and formatting parameters.
logging: This module is part of the Python standard library and is used for logging messages.
os: This module provides a way to interact with the operating system.
Logging Configuration
The script configures logging with the following settings:

Log level: The log level is set to INFO.
Log format: The log messages include the timestamp, log level, filename, and log message.
Log file: The log messages are written to a file named "project.log" in the current working directory.
Database Connection Establishment
The script connects to a SQL Server database using the pyodbc.connect() function. The connection string is constructed using the environment variables retrieved from the .env file.

get_companies() Function
The script defines a get_companies() function for retrieving company data from the API and storing it in the database. The function uses the following steps:

Constructs the API URL to retrieve company data.
Sets the filter parameters to retrieve all company records.
Makes an API request to retrieve the company data.
Iterates through the retrieved data and processes each record.
Creates a record object to store company details and inserts it into the Temp_Companies table using an SQL INSERT statement.
Logs the processed record's CompanyId.
Usage Example
The script defines the get_companies() function for retrieving and processing company data. However, it does not provide an example of calling the function or how to execute the script as a standalone program. You would need to modify the script or import it into another module to use the get_companies() function in your own application.

checkfile.py Documentation
This documentation provides an overview of the checkfile.py module, which contains two functions: validate_parameters() and remove_special_characters(). These functions are used for validating and processing parameters by removing special characters and limiting the length of the parameter value.

validate_parameters(parameters)
This function takes a parameter as input and performs the following validation steps:

Remove leading and trailing whitespaces from the parameter value using the strip() method.
Limit the length of the parameter value to 50 characters for the "Name" parameter using slicing.
Call the remove_special_characters() function to remove any special characters from the parameter value.
Assign the validated parameter value to the valid_parameter variable.
Return the validated parameter value.
remove_special_characters(value)
This function takes a value as input and removes special characters from it. It performs the following steps:

Define a list of special characters to be removed.
Iterate over the special characters list.
Use the replace() method to remove each special character from the value.
Assign the modified value back to the value variable.
Return the value with special characters removed.
Usage Example
To use the validate_parameters() and remove_special_characters() functions, import the checkfile module into your Python script or interactive session. Then, you can call these functions as needed, passing the appropriate parameters.

Here's an example:

import checkfile

# Example usage of validate_parameters()
parameter = "   example_parameter!  "
validated_parameter = checkfile.validate_parameters(parameter)
print(validated_parameter)  # Output: "example_parameter"

# Example usage of remove_special_characters()
value = "Special@Character$"
processed_value = checkfile.remove_special_characters(value)
print(processed_value)  # Output: "SpecialCharacter"

Please note that the example demonstrates how to use the functions in isolation. The validate_parameters() function is typically used within the context of the larger script where input parameters are validated before further processing.

candidates.py Documentation
This documentation provides an overview of the candidates.py module. It contains a function called get_candidates() that retrieves candidate data from an API and inserts it into a SQL Server database. The module also imports other modules and defines a class record for storing candidate data.

Import Statements
The candidates.py module imports the following modules:

apicall: This module handles API calls.
sql: This module provides functions for interacting with SQL Server.
datetime: This module provides functionality for working with dates and times.
pyodbc: This module is used for connecting to SQL Server.
checkfile: This module contains functions for parameter validation and processing.
logging: This module is used for logging messages.
dotenv_values: This function is imported from the dotenv module and is used to load environment variables from a .env file.
Function: get_candidates()
This function retrieves candidate data from an API and inserts it into a SQL Server database. It performs the following steps:

Defines a class record to hold candidate data. Each instance of the class represents a candidate record and initializes instance variables for each data field.
Constructs the API URL for retrieving candidate data.
Executes a SELECT statement to get the last run date from a table called table_updaterd.
Constructs the API request body with the necessary parameters, including the last run date as a filter.
Calls the apicall.request() function to retrieve the candidate data from the API.
Iterates over the retrieved records and creates an instance of the record class for each record.
Validates and processes the candidate data using the checkfile.validate_parameters() function.
Defines the SQL INSERT statement to insert the candidate record into the database.
Executes the SQL query using the sql.request() function.
Logs the processed record information.
Usage Example
To use the get_candidates() function, you need to import the candidates module into your Python script or interactive session. After importing, you can call the get_candidates() function.

applications.py Documentation
This documentation provides an overview of the applications.py module. It contains a function called get_applications() that retrieves application data from an API and inserts it into a SQL Server database. The module imports other modules and defines a class record for storing application data.

Import Statements
The applications.py module imports the following modules:

apicall: This module handles API calls.
sql: This module provides functions for interacting with SQL Server.
pyodbc: This module is used for connecting to SQL Server.
datetime: This module provides functionality for working with dates and times.
dateutil.parser: This module provides date parsing capabilities.
dotenv_values: This function is imported from the dotenv module and is used to load environment variables from a .env file.
logging: This module is used for logging messages.
checkfile: This module contains functions for parameter validation and processing.
Function: get_applications()
This function retrieves application data from an API and inserts it into a SQL Server database. It performs the following steps:

Defines a class record to hold application data. Each instance of the class represents an application record and initializes instance variables for each data field.
Constructs the API URL for retrieving application data.
Executes a SELECT statement to get the last run date from a table called table_updaterd.
Constructs the API request body with the necessary parameters, including the last run date as a filter.
Calls the apicall.request() function to retrieve the application data from the API.
Iterates over the retrieved records and creates an instance of the record class for each record.
Validates and processes the application data using the checkfile.validate_parameters() function.
Defines the SQL INSERT statement to insert the application record into the database.
Executes the SQL query using the sql.request() function.
Logs the processed record information.
Usage Example
To use the get_applications() function, you need to import the applications module into your Python script or interactive session. After importing, you can call the get_applications() function.

application_status_history.py Documentation
This documentation provides an overview of the application_status_history.py module. It contains a function called get_status_history() that retrieves application status history data from an API and inserts it into a SQL Server database. The module imports other modules and defines a class record for storing status history data.

Import Statements
The application_status_history.py module imports the following modules:

apicall: This module handles API calls.
sql: This module provides functions for interacting with SQL Server.
pyodbc: This module is used for connecting to SQL Server.
datetime: This module provides functionality for working with dates and times.
dateutil.parser: This module provides date parsing capabilities.
dotenv_values: This function is imported from the dotenv module and is used to load environment variables from a .env file.
logging: This module is used for logging messages.
checkfile: This module contains functions for parameter validation and processing.
Function: get_status_history()
This function retrieves application status history data from an API and inserts it into a SQL Server database. It performs the following steps:

Defines a class record to hold status history data. Each instance of the class represents a status history record and initializes instance variables for each data field.
Constructs the API URL for retrieving status history data.
Executes a SELECT statement to get the last run date from a table called table_updaterd.
Constructs the API request body with the necessary parameters, including the last run date as a filter.
Calls the apicall.request() function to retrieve the status history data from the API.
Iterates over the retrieved records and creates an instance of the record class for each record.
Validates and processes the status history data using the checkfile.validate_parameters() function.
Defines the SQL INSERT statement to insert the status history record into the database.
Executes the SQL query using the sql.request() function.
Logs the processed record information.
Usage Example
To use the get_status_history() function, you need to import the application_status_history module into your Python script or interactive session. After importing, you can call the get_status_history() function.
