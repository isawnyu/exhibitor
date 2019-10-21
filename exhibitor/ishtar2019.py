#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Objects and collections for the 2019 Ishtar exhibition
"""

from copy import deepcopy
from exhibitor.objects import ObjectCollection
import logging

logger = logging.getLogger(__name__)
ISHTAR_CROSSWALK = {
    'Catalogue Check. #': 'id',
    'Artist': 'artist',
    'Title': 'title',
    'Date': 'date',
    'Medium': 'medium',
    'Site': 'object_location',
    'Dims.': 'dimensions',
    'Lender': 'lender',
    'Object C.L.': 'credits',
    'Inv. No.': 'inventory_num',
    'Image ©': 'copyright'
}


class IshtarCollection(ObjectCollection):

    def __init__(self, crosswalk=ISHTAR_CROSSWALK):
        ObjectCollection.__init__(self, crosswalk=crosswalk)

