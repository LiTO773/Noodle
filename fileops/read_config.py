import json


def read_config() -> dict:
    """ This function reads the config file and returns it as an object """
    with open('config.json') as json_file:
        return json.load(json_file)
