#!/usr/bin/python3

import json  # parse json
from typing import Dict  # type hint iterables for older Python 3.x versions
from tempfile import TemporaryFile  # Read temporary config overrides


def get_config(temp_file: TemporaryFile = None) -> Dict:
    if temp_file is None:
        with open("config.json", 'r') as config:
            file_content = config.read()
    else:
        temp_file.seek(0)
        file_content = temp_file.read()

    config = json.loads(file_content) if len(file_content) > 0 else None
    return config


def write_temp_config(temp_file: TemporaryFile, content: Dict) -> None:
    temp_file.truncate(0)
    temp_file.seek(0)
    temp_file.write(bytes(json.dumps(content), encoding='utf-8'))
