#!/usr/bin/python3

import json  # parse json
from typing import Dict  # type hint iterables for older Python 3.x versions

def get_config() -> Dict:
    with open("config.json", 'r') as config:
        config = json.loads(config.read())

        return config
