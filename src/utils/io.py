import json


def read_txt_file(txt_file):

    with open(txt_file, "r") as f:
        TOKEN = f.read()

    return TOKEN


def write_json_file(message, address, indent=4):

    with open(address, "w") as f:

        json.dump(message, f, indent=indent)
