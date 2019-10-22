#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Prepare Ishtar data for upload
"""

from airtight.cli import configure_commandline
from exhibitor.ishtar2019 import IshtarCollection
import logging
from pathlib import Path
import sys

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
    ['source', str, 'path to Ishtar raw data JSON'],
    ['destination', str, 'path to use when outputing JSON']
]


def main(**kwargs):
    """
    main function
    """
    # logger = logging.getLogger(sys._getframe().f_code.co_name)
    source = Path(kwargs['source'])
    destination = Path(kwargs['destination'])
    ic = IshtarCollection(crosswalk=None)
    ic.load(source, 'json')
    ic.fix_titles()
    ic.make_slugs()
    sorted_slugs = sorted([(obj.data['slug'], obj.data['id']) for k, obj in ic.objects.items()], key=lambda x: x[0])
    ic.dump()
    sys.exit()
    for slug in sorted_slugs:
        print('{}:\t{}'.format(slug[0], slug[1]))
    sys.exit()
    for obj_id, obj in ic.objects.items():
        t = ''
        medium = obj.data['medium']
        if medium is None:
            medium = ''
        for fullest in ['title_detail', 'full_title', 'title']:
            if obj.data[fullest] is not None:
                t = obj.data[fullest]
                break
        print(
            '{}:{} ({}): {}'.format(
                obj_id, obj.data['slug'], medium, t
            )
        )



if __name__ == "__main__":
    main(**configure_commandline(
            OPTIONAL_ARGUMENTS, POSITIONAL_ARGUMENTS, DEFAULT_LOG_LEVEL))
