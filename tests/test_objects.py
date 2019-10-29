#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test Exhibitor objects module"""

from contextlib import contextmanager
from exhibitor.objects import ExhibitionObject, ObjectCollection
from io import StringIO
import json
import logging
from nose.tools import assert_equal, assert_false, assert_true, raises
from pathlib import Path
import sys
import textnorm
import uuid
from unittest import TestCase

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
test_data_path = Path() / 'tests' / 'data'


def setup_module():
    """Change me"""
    temp_path = test_data_path / 'out_raw_object_data.json'
    try:
        temp_path.unlink()
    except FileNotFoundError:
        pass


def teardown_module():
    """Change me"""
    temp_path = test_data_path / 'out_raw_object_data.json'
    try:
        temp_path.unlink()
    except FileNotFoundError:
        pass


@contextmanager
def captured_output():
    new_out, new_err = StringIO(), StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err


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

    def test_dump_dict(self):
        """Collection: test prep of dictionary suitable for export"""
        path = test_data_path / 'raw_object_data.csv'
        oc = ObjectCollection()
        oc.load(path)
        d = oc._make_dump_dict()
        assert_equal(3, len(d))
        for k, v in d.items():
            assert_true(k in ['foo', 'bar', 'pickle'])
        assert_equal(
            'Foo',
            d['foo']['title']
        )
        assert_equal(
            'What about foo?',
            d['foo']['summary']
        )
        assert_equal(
            'foo',
            d['foo']['id']
        )
        assert_equal(
            'foo',
            d['foo']['slug']
        )

    def test_dump_stdio_json(self):
        """Collection: test JSON dump to stdout"""
        path = test_data_path / 'raw_object_data.csv'
        oc = ObjectCollection()
        oc.load(path)
        with captured_output() as (out, err):
            oc._dump_stdio_json()
        output = out.getvalue()
        assert_equal('{', output[0])
        assert_true('"bar": {' in output)
        assert_true(
            "I don't want a pickle! I just want to ride my motorcycle!" in
            output)
        with captured_output() as (out, err):
            oc.dump()  # default is json to stdio
        output = out.getvalue()
        assert_equal('{', output[0])
        assert_true('"bar": {' in output)
        assert_true(
            "I don't want a pickle! I just want to ride my motorcycle!" in
            output)

    def test_dump_file_json(self):
        """Collection: test JSON dump to file"""
        path = test_data_path / 'raw_object_data.csv'
        oc = ObjectCollection()
        oc.load(path)
        dest = test_data_path / 'out_raw_object_data.json'
        oc.dump(dest)
        with open(dest, 'r', encoding='utf-8') as f:
            j = json.load(f)
        for k, v in j.items():
            assert_equal(v, oc.objects[k].data)

    @raises(NotImplementedError)
    def test_dump_bad_type(self):
        """Collection: test dumping to unsupported type"""
        path = test_data_path / 'raw_object_data.csv'
        oc = ObjectCollection()
        oc.load(path)
        oc.dump(file_type='rtf')

    def test_images(self):
        """Collection: test incorporating images"""
        path = test_data_path / 'raw_object_data.csv'
        oc = ObjectCollection()
        oc.load(path)
        oc.add_images(
            test_data_path / 'raw_object_images',
            None,
            fail_on_mismatch=True
        )
        wim = [o for oid, o in oc.objects.items() if o.data['image']
               is not None]
        assert_equal(3, len(wim))
        wim = [o.data['image'] for o in wim]
        assert_true('test_foo.jpg' in wim)
        assert_true('test_bar.jpg' in wim)
        assert_true('test_pickle.jpg' in wim)
        assert_true('foo_bar.tif' not in wim)
        assert_true('foobar.jpg' not in wim)

    def test_alt_text(self):
        """Collection: test adding alt_text"""
        path = test_data_path / 'raw_object_data.csv'
        oc = ObjectCollection()
        oc.load(path)
        oc._add_alt_text(
            test_data_path / 'raw_object_alt_text.csv',
            fail_on_image_missing=False,
            fail_on_mismatch=True
        )
        walt = [o for oid, o in oc.objects.items() if o.data['alt']
                is not None]
        assert_equal(3, len(walt))
        walt = [o.data['alt'] for o in walt]
        assert_true('This is an image of foo.' in walt)
        assert_true('This is an image of bar.' in walt)
        assert_true(
            'This is an image of a motorcycle in the shape of a pickle.'
            in walt)


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
