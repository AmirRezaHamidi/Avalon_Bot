def read_txt_file(txt_file):

    with open(txt_file, "r") as f:
        TOKEN = f.read()

    return TOKEN
