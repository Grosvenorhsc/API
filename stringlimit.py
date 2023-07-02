import re

def clean_and_limit_string(input_string):
    # Remove special characters except spaces
    cleaned_string = re.sub(r'[^a-zA-Z0-9 ]', '', input_string)
    
    # Limit the string to 45 characters
    limited_string = cleaned_string[:45]
    
    return limited_string