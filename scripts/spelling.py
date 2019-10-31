#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Check spelling for text fields
"""

from airtight.cli import configure_commandline
from exhibitor.ishtar2019 import PERMITTED_WORDS 
import json
import logging
from pathlib import Path
from pprint import pprint
import re
import textnorm

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
    ['words_path', str, 'path to a text file full of valid words'],
    ['json_path', str, 'path to JSON file to check']
]
rx_item_number = re.compile(
    r'^[0-9]+[a-z]+$'
)
rx_zero_padded = re.compile(
    r'^0+[0-9]+$'
)
rx_alpha_number = re.compile(
    r'^[a-z][0-9]+[a-z]?$'
)


def main(**kwargs):
    """
    main function
    """
    # logger = logging.getLogger(sys._getframe().f_code.co_name)
    wpath = Path(kwargs['words_path'])
    with open(wpath, 'r', encoding='utf-8') as f:
        good_words = f.readlines()
    del f
    good_words = [w.strip() for w in good_words]
    jpath = Path(kwargs['json_path'])
    with open(jpath, 'r', encoding='utf-8') as f:
        j = json.load(f)
    del f
    words = {}
    for oid, o in j.items():
        for k, v in o.items():
            if k in [
                'slug', 'id', 'inventory_num', 'image', 'date',
                'dimensions'
            ]:
                continue
            if v is None:
                continue
            vv = v
            for bad in [',', ':', '-', '(', ')', '.', '&', '+', '/', '–', '_', '–', ';', '[', ']', '"', '©']:
                vv = vv.replace(bad, ' ')
            vv = textnorm.normalize_space(vv)
            vv = vv.strip()
            for token in vv.split():
                try:
                    int(token)
                except ValueError:
                    pass
                else:
                    if str(int(token)) == token:
                        continue  # ignore pure numbers
                t = token.lower()
                if t in PERMITTED_WORDS:
                    continue
                if t in good_words:
                    continue
                if rx_item_number.match(t) is not None:
                    continue
                if rx_zero_padded.match(t) is not None:
                    continue
                if rx_alpha_number.match(t) is not None:
                    continue
                try:
                    words[t]
                except KeyError:
                    words[t] = []
                finally:
                    words[t].append((oid, k))
    for word in sorted(list(words.keys())):
        #print('\n\n{}\n'.format(word))
        print(word)
        for locus in words[word]:
            print('\t{}[{}]: {}'.format(
                locus[0], locus[1], j[locus[0]][locus[1]][0:80]
            ))
        #pprint(words[word], indent=4)



if __name__ == "__main__":
    main(**configure_commandline(
            OPTIONAL_ARGUMENTS, POSITIONAL_ARGUMENTS, DEFAULT_LOG_LEVEL))
