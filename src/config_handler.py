#!/usr/bin/python3

import json  # parse json


def get_config() -> dict:
    with open("config.json", 'r') as config:
        config = json.loads(config.read())

        return config
