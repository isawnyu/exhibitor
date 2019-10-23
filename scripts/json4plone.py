#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Prepare Exhibition Object JSON for upload to Plone
"""

from airtight.cli import configure_commandline
import json
import logging
from pathlib import Path
from pprint import pprint

logger = logging.getLogger(__name__)

DEFAULT_LOG_LEVEL = logging.WARNING
OPTIONAL_ARGUMENTS = [
    ['-l', '--loglevel', 'NOTSET',
        'desired logging level (' +
        'case-insensitive string: DEBUG, INFO, WARNING, or ERROR',
        False],
    ['-v', '--verbose', False, 'verbose output (logging level == INFO)',
        False],
    ['-w', '--veryverbose', False,
        'very verbose output (logging level == DEBUG)', False],
]
POSITIONAL_ARGUMENTS = [
    # each row is a list with 3 elements: name, type, help
    ['url_path', str, 'path on the server where the collection will reside'],
    ['source', str, 'path to exhibitor JSON'],
    ['destination', str, 'path to use when outputing plone-ready JSON']
]


def main(**kwargs):
    """
    main function
    """
    # logger = logging.getLogger(sys._getframe().f_code.co_name)
    source = Path(kwargs['source'])
    destination = Path(kwargs['destination'])
    with open(source, 'r', encoding='utf-8') as f:
        j = json.load(f)
    del f
    items = []
    for orig_id, obj_data in j.items():
        item = {}
        for field_name, field_value in obj_data.items():
            if field_name not in ['id', 'slug']:
                if field_value is not None:
                    item[field_name] = field_value
        item['id'] = obj_data['slug']
        items.append(item)
    payload = {
        'items': []
    }
    for item in items:
        payload['items'].append(
            {
                kwargs['url_path']: item
            }
        )
    with open(destination, 'w', encoding='utf-8') as f:
        json.dump(payload, f, ensure_ascii=False, indent=4, sort_keys=True)
    del f


if __name__ == "__main__":
    main(**configure_commandline(
            OPTIONAL_ARGUMENTS, POSITIONAL_ARGUMENTS, DEFAULT_LOG_LEVEL))
