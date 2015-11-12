import os
import json

key_file = "api_key.txt"
path = os.path.join(os.path.dirname(os.path.realpath(__file__)), key_file)

with open(path, 'r') as data_file:
    keys = json.load(data_file)