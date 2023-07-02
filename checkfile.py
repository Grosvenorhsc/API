def validate_parameters(parameters):
   
        # Remove leading/trailing whitespaces
        value = parameters.strip()

        # Limit the length to 50 characters for 'Name' parameter
        value = value[:50]

        # Check for special characters
        value = remove_special_characters(value)

        # Add the validated parameter to the dictionary
        valid_parameter = value

        return valid_parameter

def remove_special_characters(value):
    # Define a list of special characters to be removed
    special_characters = ['!', '@', '#', '$', '%', '^', '&', '*']

    # Remove special characters from the value
    for char in special_characters:
        value = value.replace(char, '')

    return value