import json
import os

def read_db(file_name):
    if os.path.exists(file_name):
        try:
            with open(file_name, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("Error: File is not a valid JSON.")
            return {}
    else:
        print(f"Error: file {file_name} is not existed")

    return {}

def write_db(file_name, data):
    with open(file_name, 'w') as f:
        json.dump(data, f, indent=2)