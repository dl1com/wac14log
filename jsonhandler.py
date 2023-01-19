import json

def read_contest_info(filename):
    f = open(filename)
    data = json.load(f)
    f.close()
    return data