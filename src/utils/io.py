import json

def write_json(data, json_file, indent=4):

    with open(json_file, "w") as f:
        json.dump(data.json, f, indent=indent)
