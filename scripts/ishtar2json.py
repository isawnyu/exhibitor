#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Convert raw Ishtar CSV to clean JSON
"""

from airtight.cli import configure_commandline
from exhibitor.ishtar2019 import IshtarCollection
import logging
from pathlib import Path

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
    ['source', str, 'path to Ishtar raw data CSV'],
    ['destination', str, 'path to use when outputing JSON']
]


def main(**kwargs):
    """
    main function
    """
    # logger = logging.getLogger(sys._getframe().f_code.co_name)
    source = Path(kwargs['source'])
    destination = Path(kwargs['destination'])
    ic = IshtarCollection()
    ic.load(source, merge=True)
    ic.dump(file_path=destination)
    print('Saved result file at {}'.format(destination.absolute()))


if __name__ == "__main__":
    main(**configure_commandline(
            OPTIONAL_ARGUMENTS, POSITIONAL_ARGUMENTS, DEFAULT_LOG_LEVEL))
