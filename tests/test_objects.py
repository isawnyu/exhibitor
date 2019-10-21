#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test Exhibitor objects module"""

from exhibitor.objects import ExhibitionObject, ObjectCollection
import logging
from nose.tools import assert_equal, assert_false, assert_true, raises
from pathlib import Path
import textnorm
import uuid
from unittest import TestCase

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
test_data_path = Path() / 'tests' / 'data'


def setup_module():
    """Change me"""
    pass


def teardown_module():
    """Change me"""
    pass


class Test_Collection(TestCase):

    def setUp(self):
        """Change me"""
        pass

    def tearDown(self):
        """Change me"""
        pass

    def test_instantiate(self):
        """Collection: instantiate"""
        oc = ObjectCollection()
        assert_equal(0, len(oc))

    def test_make_obj(self):
        """Collection: make object"""
        oc = ObjectCollection()
        d = {
            'id': 'foo',
            'slug': 'foo',
            'title': 'Foo',
            'summary': 'Some information about the foo object.'
        }
        o_id, o = oc._make_object(d, None)
        assert_equal('foo', o_id)
        for k, v in d.items():
            assert_equal(v, o.data[k])

    def test_make_with_obj(self):
        """Collection: make object with existing object"""
        d = {
            'id': 'foo',
            'slug': 'foo',
            'title': 'Foo',
            'summary': 'Some information about the foo object.'
        }
        o = ExhibitionObject(d)
        oc = ObjectCollection()
        oo_id, oo = oc._make_object(o, None)
        assert_equal('foo', oo_id)
        assert_equal(o, oo)

    def test_make_with_obj_override(self):
        """Collection: make object with existing and override id"""
        d = {
            'id': 'foo',
            'slug': 'foo',
            'title': 'Foo',
            'summary': 'Some information about the foo object.'
        }
        o = ExhibitionObject(d)
        oc = ObjectCollection()
        oo_id, oo = oc._make_object(o, 'bar')
        assert_equal('bar', oo_id)
        assert_equal('bar', oo.data['id'])

    def test_add(self):
        """Collection: test adding object to collection"""
        oc = ObjectCollection()
        d = {
            'id': 'foo',
            'slug': 'foo',
            'title': 'Foo',
            'summary': 'Some information about the foo object.'
        }
        oc.add(d)
        assert_equal(1, len(oc))
        objs = [v for k, v in oc.objects.items()]
        for k, v in d.items():
            assert_equal(v, objs[0].data[k])

    @raises(RuntimeError)
    def test_add_collision(self):
        """Collection: test adding objects with id collision"""
        oc = ObjectCollection()
        d = {
            'id': 'foo',
            'slug': 'foo',
            'title': 'Foo',
            'summary': 'Some information about the foo object.'
        }
        oc.add(d)
        q = {
            'id': 'foo',
            'slug': 'bar',
            'title': 'Bar',
            'summary': 'Some information about the bar object.'
        }
        oc.add(q)

    def test_load(self):
        """Collection: load from file"""
        path = test_data_path / 'raw_object_data.csv'
        oc = ObjectCollection()
        oc.load(path)
        assert_equal(3, len(oc.objects))

    @raises(NotImplementedError)
    def test_load_rtf(self):
        """Collection: reject loading rtf from file"""
        path = test_data_path / 'raw_object_data.rtf'
        oc = ObjectCollection()
        oc.load(path, file_type='rtf')
        

class Test_Object(TestCase):

    def test_instantiate_internal(self):
        """Object: instantiate with internal id"""
        d = {
            'id': 'foo',
            'slug': 'foo',
            'title': 'Foo',
            'summary': 'Some information about the foo object.'
        }
        o = ExhibitionObject(d)
        for k, v in d.items():
            assert_equal(v, o.data[k])

    def test_instantiate_external(self):
        """Object: instantiate with external id"""
        d = {
            'slug': 'foo',
            'title': 'Foo',
            'summary': 'Some information about the foo object.'
        }
        o = ExhibitionObject(d, 'foo')
        assert_equal('foo', o.data['id'])
        for k, v in d.items():
            assert_equal(v, o.data[k])

    def test_instantiate_uuid(self):
        """Object: instantiate with generated id"""
        d = {
            'slug': 'foo',
            'title': 'Foo',
            'summary': 'Some information about the foo object.'
        }
        o = ExhibitionObject(d)
        assert_true(uuid.UUID(o.data['id'], version=4))

    @raises(RuntimeError)
    def test_instantiate_conflict(self):
        """Object: fail with conflicting internal and external ids"""
        d = {
            'id': 'foo',
            'slug': 'foo',
            'title': 'Foo',
            'summary': 'Some information about the foo object.'
        }
        ExhibitionObject(d, 'bar')

    @raises(ValueError)
    def test_unadaptable(self):
        """Object: fail with unadaptable parameters"""
        d = ['foo', 'foo', 'foo', 'A summery summary.']
        ExhibitionObject(d)

    def test_crosswalk(self):
        """Object: instantiate with crosswalk"""
        d = {
            'identifier': 'foo',
            'short_title': 'foo',
            'title': 'Foo',
            'description': 'Some information about the foo object.'
        }
        x = {
            'identifier': 'id',
            'short_title': 'slug',
            'title': 'title',
            'description': 'summary'
        }
        o = ExhibitionObject(d, crosswalk=x)
        assert_equal('foo', o.data['id'])
        assert_equal('foo', o.data['slug'])
        assert_equal('Foo', o.data['title'])
        assert_equal(
            'Some information about the foo object.',
            o.data['summary'])

    def test_cleanup(self):
        """Object: test instantiate with unclean data"""
        d = {
            'id': 'foo',
            'slug': 'foo',
            'title': '\nFoo lish ',
            'summary': textnorm.normalize_unicode(
                'μ\u03adγα βιβλ\u03afον μ\u03adγα κακ\u03ccν',
                'NFC'
            )
        }
        o = ExhibitionObject(d)
        assert_equal('Foo lish', o.data['title'])
        assert_equal('μέγα βιβλίον μέγα κακόν', o.data['summary'])

    def test_merge(self):
        """Object: test merge with another objects"""
        d1 = {
            'id': 'foo',
            'slug': 'foo',
            'title': 'Foo',
            'summary': 'Some information about the foo object.'
        }
        d2 = {
            'id': 'bar',
            'slug': 'bar',
            'title': 'Bar',
            'summary': 'Some information about the bar object.'
        }
        o1 = ExhibitionObject(d1)
        o2 = ExhibitionObject(d2)
        o3 = o1.merge(o2)
        assert_true(uuid.UUID(o3.data['id'], version=4))

