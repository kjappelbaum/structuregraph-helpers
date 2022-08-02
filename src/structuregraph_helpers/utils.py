import json


def dump_json(data, filename):
    with open(filename, "w") as f:
        json.dump(data, f)
