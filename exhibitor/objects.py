#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exhibition Objects and Collections of Same
"""

from copy import deepcopy
from encoded_csv import get_csv
import json
import logging
from slugify import slugify
import textnorm
import uuid


# exhibition object fields are defined at:
# github.com/isawnyu/isaw.web:
#    /src/isaw.exhibitions/isaw/exhibitions/interfaces/__init__.py

fields = [
    'title',  # required
    'summary',  # plone calls this "description", but what's labeled
                # "description" in base view is actually "full_title"
    'full_title',
    'title_detail',
    'artist',
    'author',
    'copyist',
    'download_link',
    'download_link_text',
    'download_link_type',
    'translator',
    'copyright',
    'credits',
    'date',
    'dimensions',
    'exhibition_context',
    'image',
    'alt',
    'inventory_num',  # required
    'lender',
    'lender_link',
    'medium',
    'not_after',
    'not_before',
    'notes',
    'object_language',
    'object_location',
    'text',  # i.e. body
    'label',
    'id',
    'title',
    'slug',
    'summary'
]
required_fields = [
    'title',
    'inventory_num'
]
logger = logging.getLogger(__name__)


class ExhibitionObject(object):
    """
    Information about a single item (or group of items) in an exhibition.
    One exhibition object corresponds to a single "object" page on
    the ISAW website.
    """

    def __init__(self, obj_data, obj_id=None, crosswalk=None):
        valid = False
        for valid_type in [dict]:
            if isinstance(obj_data, valid_type):
                valid = True
                break
        if not valid:
            msg = 'Unable to adapt object data of type {}'.format(
                type(obj_data))
            raise ValueError(msg)
        self.data = {}
        for field in fields:
            self.data[field] = None
        try:
            internal_id = obj_data['id']
        except KeyError:
            internal_id = None
        if obj_id is None:
            if internal_id is None:
                this_id = str(uuid.uuid4())
            else:
                this_id = internal_id
        else:
            this_id = obj_id
            if internal_id is not None:
                if internal_id != obj_id:
                    msg = (
                        'internal_id({}) does not match obj_id({})'
                        ''.format(internal_id, obj_id)
                    )
                    raise RuntimeError(msg)
        self.data['id'] = this_id
        self._adapt(
            {k: v for k, v in obj_data.items() if k != 'id'}, crosswalk)

    def merge(self, other_obj, delimiter='; '):
        merged = {}
        for k, this_v in self.data.items():
            if k == 'id':
                continue
            try:
                other_v = other_obj.data[k]
            except KeyError:
                other_v = None
            if this_v is None and other_v is None:
                merged[k] = None
            elif this_v is None:
                merged[k] = other_v
            elif other_v is None:
                merged[k] = this_v
            else:
                if this_v == other_v:
                    merged[k] = this_v
                else:
                    merged[k] = delimiter.join((this_v, other_v))
        merged['id'] = str(uuid.uuid4())
        return ExhibitionObject(merged)

    def _adapt(self, obj_data, crosswalk):
        if crosswalk is None:
            xwalk = {}
            for k in self.data.keys():
                if k != 'id':
                    xwalk[k] = k
        else:
            xwalk = crosswalk
        for k, v in obj_data.items():
            if k != 'id':
                self.data[xwalk[k]] = self._clean_value(v)

    def _clean_value(self, raw_value):
        v = raw_value
        if v is not None:
            v = textnorm.normalize_space(v)
            v = textnorm.normalize_unicode(v, 'NFC')
            if v in ['', ' ']:
                v = None
        return v


class ObjectCollection(object):

    def __init__(self, crosswalk=None):
        self.objects = {}
        self.indices = {}
        self.slugs = {}
        self.crosswalk = crosswalk

    def __len__(self):
        return len(self.objects)

    def add(self, obj_data, obj_id=None, merge=False):
        this_id, this_obj = self._make_object(obj_data, obj_id)
        try:
            self.objects[this_id]
        except KeyError:
            self.objects[this_id] = this_obj
        else:
            if merge:
                logger.warning(
                    'Merging objects with id={}. You may want to check title.'
                    ''.format(this_id)
                )
                merged_obj = self.objects[this_id].merge(this_obj)
                merged_obj.data['id'] = this_id
                self.objects[this_id] = merged_obj
            else:
                msg = (
                    'ID collision in object addition: there is already a key '
                    'with value "{}"'
                    ''.format(this_id)
                )
                raise RuntimeError(msg)
        try:
            del self.indices['title']
        except KeyError:
            pass

    def dump(self, file_path=None, file_type='json'):
        valid_types = ['json']
        if file_type not in valid_types:
            raise NotImplementedError(
                'Dumping an object collection to a file of type "{}" '
                'is unsupported. Supported types: {}'
                ''.format(file_type, valid_types)
            )
        elif file_path is None:
            getattr(
                self,
                '_dump_stdio_{}'.format(file_type))()
        else:
            getattr(
                self,
                '_dump_file_{}'.format(file_type))(file_path)

    def get_by_title(self, title):
        try:
            self.indices['title']
        except KeyError:
            self.indices['title'] = {}
            for obj_id, obj in self.objects.items():
                try:
                    self.indices['title'][obj.data['title']]
                except KeyError:
                    self.indices['title'][obj.data['title']] = [obj_id]
                else:
                    self.indices['title'][obj.data['title']].append(obj_id)
        try:
            return self.indices['title'][title]
        except KeyError:
            return []

    def load(self, path, file_type='csv', merge=False):
        valid_types = ['csv', 'json']
        if file_type not in valid_types:
            raise NotImplementedError(
                'Loading an object collection from a file of type "{}" '
                'is unsupported. Supported types: {}'
                ''.format(file_type, valid_types)
            )
        elif file_type == 'csv':
            data = get_csv(path, sample_lines=1000)
            for datum in data['content']:
                self.add(datum, merge=merge)
        elif file_type == 'json':
            with open(path, 'r', encoding='utf8') as f:
                j = json.load(f)
            del f
            for datum_id, datum in j.items():
                self.add(datum, obj_id=datum_id, merge=merge)

    def make_slugs(self):
        for obj_id, obj in self.objects.items():
            slug = self._set_slug(obj_id)
            if slug is None:
                slug = obj.data['title']
                for punct in [':', '(', '.', ';', ',']:
                    if punct in slug:
                        slug = slug.split(punct)[0].strip()
                slug = textnorm.normalize_space(slug)
                words = slug.split()
                for skip in ['of', 'with', 'from']:
                    try:
                        idx = words.index(skip)
                    except ValueError:
                        continue
                    else:
                        del words[idx]
                slug = ' '.join(words)
                slug = slugify(slug, only_ascii=True)
            try:
                self.slugs[slug]
            except KeyError:
                self.slugs[slug] = 1
            else:
                suffix = chr(self.slugs[slug] + 96)
                self.slugs[slug] += 1
                slug += '-{}'.format(suffix)
            obj.data['slug'] = slug

    def make_summaries(self, exhibition_blurb=None):
        for obj_id, obj in self.objects.items():
            summary = self._set_summary(obj, exhibition_blurb)
            if summary is None:
                raise RuntimeError('Disastrous fail')
            else:
                obj.data['summary'] = summary

    def _make_summary_artist(self, obj, suppress_unknown=True):
        artist = obj.data['artist']
        if artist is not None:
            if not suppress_unknown or 'unknown' not in artist.lower():
                return artist
        return None

    def _make_summary_inventory_num(self, obj, suppress_unknown=True):
        invno = obj.data['inventory_num']
        if invno is not None:
            if (
                not suppress_unknown or
                (
                    'unknown' not in invno and
                    invno != 'N/A'
                )
            ):
                return invno
        return None

    def _make_summary_lender(self, obj):
        return obj.data['lender']

    def _make_summary_location(self, obj):
        return obj.data['object_location']

    def _make_summary_title(self, obj, include_detail=False):
        title_types = ['full_title', 'title']
        if include_detail:
            title_types = ['title_detail'] + title_types
        for fullest in title_types:
            if obj.data[fullest] is not None:
                return obj.data[fullest]
        raise RuntimeError(
            'No valid titles in object {}'.format(obj.data['id'])
        )

    def _dump_file_json(self, file_path):
        d = self._make_dump_dict()
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(
                d,
                f,
                ensure_ascii=False,
                indent=4,
                sort_keys=True
            )

    def _dump_stdio_json(self):
        d = self._make_dump_dict()
        j = json.dumps(
            d,
            ensure_ascii=False,
            indent=4,
            sort_keys=True
        )
        print(j)

    def _make_dump_dict(self):
        d = {}
        for obj_id, obj in self.objects.items():
            d[obj_id] = obj.data
        return d

    def _make_object(self, obj_data, obj_id):
        if isinstance(obj_data, ExhibitionObject):
            if obj_id is None:
                return (obj_data.data['id'], obj_data)
            else:
                new_obj = deepcopy(obj_data)
                new_obj.data['id'] = obj_id
                return (obj_id, new_obj)
        else:
            o = ExhibitionObject(obj_data, obj_id, self.crosswalk)
            return (o.data['id'], o)

    def _set_slug(self, obj_id):
        return None

    def _set_summary(self, obj, exhibition_blurb):
        summary = ''
        summary += self._make_summary_title(obj)
        artist = self._make_summary_artist(obj)
        if artist is not None:
            summary += ' by {}'.format(artist)
        ol = self._make_summary_location(obj)
        if ol is not None:
            summary += ' from {}'.format(ol)
        summary += '. '
        summary += 'Lent by {} (inventory number: {}).'.format(
            obj._make_summary_lender(), 
            obj._make_summary_inventory_number())
        if exhibition_blurb is not None:
            summary += ' {}'.format(exhibition_blurb)
        if summary[-1] != '.':
            summary += '.'
        return summary


