#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test exhibitor for ishtar 2019"""

from exhibitor.ishtar2019 import IshtarCollection, ISHTAR_CROSSWALK
import logging
from nose.tools import assert_equal, assert_false, assert_true, raises
from os.path import abspath, join, realpath
from pathlib import Path
from unittest import TestCase

logger = logging.getLogger(__name__)
test_data_path = Path() / 'tests' / 'data'


def setup_module():
    """Change me"""
    pass


def teardown_module():
    """Change me"""
    pass


class Test_Ishtar(TestCase):

    def setUp(self):
        """Change me"""
        pass

    def tearDown(self):
        """Change me"""
        pass

    def test_collection_instantiate(self):
        """IshtarCollection: Test Instantiation"""
        ic = IshtarCollection()
        assert_equal(ISHTAR_CROSSWALK, ic.crosswalk)

    def test_object_load(self):
        ic = IshtarCollection()
        ic.load(test_data_path / 'ishtar_2019-08-21.csv', merge=True)
        assert_equal(133, len(ic))
        brick_frags = ic.get_by_title('Brick fragment')
        assert_equal(1, len(brick_frags))
        bf = ic.objects[brick_frags[0]]
        assert_equal('Brick fragment', bf.data['title'])
        assert_true(bf.data['inventory_num'].startswith('VA 17462; VA 17479'))
