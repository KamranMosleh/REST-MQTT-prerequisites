import json
import os  # to go beyond the Python environment for file path handling, and file management.
# e.g.: create or delete files or folders, rename files, and even run other programs.

# Get the path of the current script
script_path = os.path.abspath(__file__)
# Get the current directory of the script
script_dir = os.path.dirname(script_path)
json_file_name = 'CherryPy_JSON_handling_dump.json'
# Define the path of the JSON file in the current directory
json_file_path = os.path.join(script_dir, json_file_name)

# create a JSON file and write data to it
data = {'temperature': 25.5, 'humidity': 60 } # data to be written to JSON file (dictionary)
# Save the JSON data to the file
with open(json_file_path, 'w') as json_file_data:
    json.dump(data, json_file_data, indent=4)  # indent for pretty printing (optional)


# CherryPy_JSON_handling_dump.json will contain:
# {
#     "temperature": 25.5,
#     "humidity": 60
# }