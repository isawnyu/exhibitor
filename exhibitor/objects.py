#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exhibition Objects and Collections of Same
"""

import logging

logger = logging.getLogger(__name__)


class ObjectCollection(object):

    def __init__(self):
        self.objects = {}

    def __len__(self):
        return len(self.objects)
