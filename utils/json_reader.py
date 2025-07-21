import json
import os


def load_json_data(file_name):
    file_path = os.path.join("test_data", file_name)
    with open(file_path, "r") as f:
        return json.load(f)
