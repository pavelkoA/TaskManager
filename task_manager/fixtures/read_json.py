import json
import os


def load_json(json_file):
    with open(os.path.abspath(f'task_manager/fixtures/{json_file}'), 'r') as file:
        return json.loads(file.read())
