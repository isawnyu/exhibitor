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


TITLE_FIXUPS = {
    "1": {
        'original_title': 'Crate used to ship bricks from Babylon to Berlin',
        'title': 'Shipping Crate'
    },
    "10": {
        'original_title': (
            "Fragmentary brick with floral motif and fitters' mark"
        ),
        'title': 'Brick'
    },
    "100": {
        'original_title': 'Bowl with procession of bulls',
        'title': 'Bowl with Bulls'
    },
    "102": {
        'original_title': (
            'Stamp seal and modern impression with a worshipper or priest '
            'before the divine symbols of Marduk (spade) and Nabu (stylus) on '
            'a mušhuššu-dragon altar (on face), a dog and lamp or incense '
            'burner (on sides)'),
        'title': 'Stamp Seal',
        'full_title': 'Stamp seal and modern impression',
        'title_detail': 'original_title'
    },
    "104": {
        'original_title': 'Reconstruction of a brick with lion fur',
        'title': 'Illustration',
    },
    "105": {
        'original_title': (
            "Partial reconstruction of throne room façade from Nebuchadnezzar "
            "II's Southern Palace showing fitters' marks on bricks"),
        'title': 'Illustration',
        'full_title': 'Partial reconstruction of throne room façade',
        'title_detail': 'original_title',
    },
    "106": {
        'original_title': (
            "Partial reconstruction of a wall from Nebuchadnezzar II's "
            "Southern Palace showing fitters' marks on bricks, based on "
            "collapsed remains found in situ"),
        'title': 'Illustration',
        'full_title': 'Partial reconstruction of palace wall',
        'title_detail': 'original_title'
    },
    "107": {
        'original_title': (
            "Portion of glazed brick wall showing rosette decoration and "
            "bitumen found in situ"),
        'title': 'Illustration',
        'full_title': 'Portion of glazed brick wall',
        'title_detail': 'original_title'
    },
    "108": {
        'original_title': (
            "Reconstruction of bricks with a mušhuššu-dragon from the Ishtar "
            "Gate"
        ),
        'title': 'Illustration'
    },
    '109': {
        'original_title': 'Reconstruction of the Ishtar Gate façade',
        'title': 'Illustration'
    },
    "11": {
        'original_title': (
            "Fragmentary brick with impression of reed matting, and a dog's "
            "paw print on reverse"
        ),
        'title': 'Brick'
    },
    '110': {
        'original_title': 'Reconstruction of the Ishtar Gate',
        'title': 'Illustration'
    },
    '111': {
        'original_title': (
            "Eyestone with cuneiform inscription of Nebuchadnezzar II "
            "(dedication to the god Marduk)"
        ),
        'title': 'Eyestone',
        'full_title': 'Eyestone with cuneiform inscription',
        'title_detail': 'original_title'
    },
    '112': {
        'original_title': (
            "Cylinder seal and modern impression with an enthroned figure and "
            "a kneeling bull supporting a winged gate"),
        'title': 'Cylinder Seal',
        'full_title': 'Cylinder Seal and Modern Impression',
        'title_detail': 'original_title'
    },
    '113': {
        'original_title': (
            "Cylinder seal and modern impression with contest between lion and "
            "bull"),
        'title': 'Cylinder Seal',
        'full_title': 'Cylinder Seal and Modern Impression',
        'title_detail': 'original_title'
    },
    '114': {
        'original_title': (
            "Cylinder seal and modern impression with a divine hero in contest "
            "with a lion"),
        'title': 'Cylinder Seal',
        'full_title': 'Cylinder Seal and Modern Impression',
        'title_detail': 'original_title'
    },
    '115': {
        'original_title': (
            "Cylinder seal and modern impression with a worshipper or priest "
            "before the divine symbols of Marduk (spade) and Nabu (stylus), "
            "and a god on a lion monster"),
        'title': 'Cylinder Seal',
        'full_title': 'Cylinder Seal and Modern Impression',
        'title_detail': 'original_title'
    },
    '116': {
        'original_title': (
            "Cylinder seal and modern impression with a king in contest with "
            "two lions"),
        'title': 'Cylinder Seal',
        'full_title': 'Cylinder Seal and Modern Impression',
        'title_detail': 'original_title'
    },
    '117': {
        'original_title': (
            "Bricks with a protective bull-man and cuneiform inscription"),
        'title': 'Inscribed Bricks'
    },
    '118': {
        'original_title': 'Fragmentary brick with the hand of a queen',
        'title': 'Brick'
    },
    '119': {
        'original_title': 'Fragmentary brick with a cuneiform inscription',
        'title': 'Inscribed Brick'
    },
    '12': {
        'original_title': (
            "Fragmentary brick stamped with cuneiform inscription of "
            "Nebuchadnezzar II and impressed with a dog's paw print"
        ),
        'title': 'Inscribed Brick'
    },
    '120': {
        'original_title': (
            "Fragmentary tile with a genie standing on two griffins in contest with two monsters"
        ),
        'title': 'Tile'
    },
    '121': {
        'original_title': 'Fragmentary wall tile with checkerboard motif',
        'title': 'Tile'
    },
    '122': {
        'original_title': 'Bricks with the head of an archer',
        'title': 'Bricks'
    },
    '123': {
        'original_title': 'Mold for a female figurine',
        'title': 'Mold'
    },
    '124': {
        'original_title': (
            "Sample of eye agate; Sample of blue chalcedony; Sample of "
            "polished blue chalcedony; Sample of rock crystal; Sample of lapis "
            "lazuli; Sample of sandstone; Sample of alluvial quartz pebbles; "
            "Sample of lead; Sample of copper; Sample of tin; Sample of "
            "antimony; Sample of erythrite; Sample of iron"
        ),
        'title': 'Mineral Samples',
        'full_title': 'Samples of stones and metals',
        'title_detail': (
            'Samples of eye agate, blue chalcedony, polished blue chalcedony, '
            'rock crystal, lap lazuli, sandstone, alluvial quartz pebbles, '
            'lead, copper, tin, antimony, erythrite, and iron.'
        )
    },
    '125': {
        'original_title': (
            'Stela of Ashurbanipal carrying a ritual basket of earth, '
            'with cuneiform inscription'
        ),
        'title': 'Inscribed Stela',
        'full_title': 'Inscribed Stela of Ashurbanipal',
        'title_detail': 'original_title'
    },
    '126': {
        'original_title': (
            "Brick stamped with cuneiform inscription of Nebuchadnezzar II and"
            " incised with alphabetic worker's inscription (zbn')"
        ),
        'title': 'Inscribed Brick',
        'full_title': 'Brick stamped with cuneiform inscription',
        'title_detail': 'original_title'
    },
    '127': {
        'original_title': 'Brick with the head and wings of a protective genie',
        'title': 'Brick'
    },
    '128': {
        'original_title': 'Cuneiform tablet with a red glass recipe',
        'title': 'Cuneiform Tablet'
    },
    '129': {
        'original_title': 'Fragmentary cuneiform tablet with glass recipes',
        'title': 'Cuneiform Tablet'
    },
    '13': {
        'original_title': (
            "Brick stamped with alphabetic worker's inscription (lqṣr') and a "
            "lion surrounded by body parts"
        ),
        'title': 'Inscribed Brick'
    },
    '131': {
        'original_title': (
            "Cylinder seal and modern impression with the creator god Enki/Ea "
            "in his watery realm (apsû)"
        ),
        'title': 'Cylinder Seal',
        'full_title': 'Cylinder Seal and Modern Impression',
        'title_detail': 'original_title'
    },
    '132': {
        'original_title': (
            "Cylinder seal and modern impression with a worshipper or priest "
            "before the goddess Ishtar standing on a lion"
        ),
        'title': 'Cylinder Seal',
        'full_title': 'Cylinder Seal and Modern Impression',
        'title_detail': 'original_title'
    },
    '133': {
        'original_title': (
            "Cylinder seal and modern impression with two worshippers or "
            "priests, one before the moon-god Sin in a crescent, and one "
            "before the divine symbol of Marduk (spade) on a mušhuššu-dragon "
            "altar"
        ),
        'title': 'Cylinder Seal',
        'full_title': 'Cylinder Seal and Modern Impression',
        'title_detail': 'original_title'
    },
    '14': {
        'original_title': (
            "Brick fragment incised with alphabetic worker's inscription "
            "(zbn')"
        ),
        'title': 'Inscribed Brick'
    },
    '15': {
        'original_title': (
            "Brick fragment stamped with alphabetic worker's inscription (nb)"
        ),
        'title': 'Inscribed Brick'
    },
    '16': {
        'original_title': "Brick with the head of a water goddess",
        'title': 'Brick'
    },
    '17': {
        'original_title': (
            'Brick with the neck and hair of a water goddess, with spouting '
            'water'
        ),
        'title': 'Brick'
    },
    '18': {
        'original_title': 'Brick with the head of a mountain god',
        'title': 'Brick'
    },
    '19': {
        'original_title': (
            "Brick with the beard and hair of a mountain god, with spouting "
            "water"
        ),
        'title': 'Brick'
    },
    '20': {
        'original_title': (
            'Wall tile with knob, decorated with palmette and eye motifs'
        ),
        'title': 'Wall Tile'
    },
    '21': {
        'original_title': (
            "Brick with part of a god's face and fitters' marks"
        ),
        'title': 'Brick'
    },
    '22': {
        'original_title': 'Reconstructed brick with floral motif',
        'title': 'Reconstructed Brick'
    },
    '23': {
        'original_title': 'Brick fragment with rosette motif',
        'title': 'Brick'
    },
    '24': {
        'original_title': 'Brick fragment with rosette motif',
        'title': 'Brick'
    },
    '25': {
        'original_title': 'Brick fragment with rosette motif',
        'title': 'Brick'
    },
    '26': {
        'original_title': 'Vessel with frieze of kneeling caprids',
        'title': 'Vessel'
    },
    '28': {
        'original_title': (
            'Fragmentary mold for a female figurine and modern cast'
        ),
        'title': 'Mold'
    },
    '29': {
        'original_title': (
            "Foundation figurine of a protective apkallu-sage wearing a fish "
            "skin"
        ),
        'title': "Foundation Figurine"
    },
    '3': {
        'original_title': 'Brick with the underbelly of a bull',
        'title': 'Brick'
    },
    '31': {
        'original_title': (
            'Cylinder seal and modern impression with a divine hero in '
            'contest with a bull'
        ),
        'title': 'Cylinder Seal',
        'full_title': 'Cylinder Seal and Modern Impression',
        'title_detail': 'original_title'
    },
    '34': {
        'original_title': (
            'Hair- or beard-curl inlay from a composite statuette'
        ),
        'title': 'Inlay from Statuette'
    },
    '35': {
        'original_title': (
            'Hair- or beard-curl inlay from a composite statuette'
        ),
        'title': 'Inlay from Statuette'
    },
    '36': {
        'original_title': (
            'Fragmentary hair or beard inlay from a composite statuette'
        ),
        'title': 'Inlay from Statuette'
    },
    '37': {
        'original_title': (
            'Fragmentary hair- or beard-curl inlay from a composite statuette'
        ),
        'title': 'Inlay from Statuette'
    },
    '38': {
        'original_title': (
            'Fragmentary hair or beard inlay from a composite statue'
        ),
        'title': 'Inlay from Statue'
    },
    '39': {
        'original_title': (
            'Fragmentary hair or beard inlay from a composite statue'
        ),
        'title': 'Inlay from Statue'
    },
    '4': {
        'original_title': 'Brick with a mušhuššu-dragon neck',
        'title': 'Brick'
    },
    '40': {
        'original_title': (
            "Divine cylinder seal with the god Marduk and cuneiform "
            "inscription (dedication by Marduk-zakir-shumi I)"
        ),
        'title': 'Cylinder Seal',
        'full_title': 'Divine Cylinder Seal',
        'title_detail': 'original_title'
    },
    '44': {
        'original_title': (
            "Relief with a god (possibly Ashur) on a lion monster, and divine "
            "symbols"
        ),
        'title': 'Relief'
    },
    '45': {
        'original_title': (
            "Reconstruction of bricks with a mušhuššu-dragon from the Ishtar "
            "Gate"
        ),
        'title': 'Reconstructed Bricks'
    },
    '46': {
        'original_title': (
            "Reconstruction of a bull from the Ishtar Gate"
        ),
        'title': 'Reconstructed Bull'
    },
    '47': {
        'original_title': (
            'Beginning of excavation of the Ishtar Gate'
        ),
        'title': 'Excavation Photograph'
    },
    '48': {
        'original_title': (
            "Portion of an Ishtar Gate wall found in situ, showing an earlier "
            "unglazed molded bull and part of a later glazed flat bull"
        ),
        'title': 'Excavation Photograph',
        'full_title': 'Portion of an Ishtar Gate wall found in situ',
        'title_detail': 'original_title'
    },
    '49': {
        'original_title': (
            "Portion of an Ishtar Gate wall with unglazed mušhuššu-dragon "
            "bricks found in situ"
        ),
        'title': 'Excavation Photograph',
        'full_title': 'Portion of an Ishtar Gate wall found in situ',
        'title_detail': 'original_title'
    },
    '5': {
        'original_title': 'Brick with cuneiform sign bi',
        'title': 'Brick'
    },
    '50': {
        'original_title': (
            'View of unglazed remains of the Ishtar Gate found in situ'),
        'title': 'Excavation Photograph'
    },
    '51': {
        'original_title': (
            'Remains of unglazed walls of the Ishtar Gate found in situ'),
        'title': 'Excavation Photograph'
    },
    '52': {
        'original_title': (
            'Desalinating glazed brick fragments from Babylon'
        ),
        'title': 'Curatorial Photograph'
    },
    '53': {
        'original_title': (
            'Sorting and assembling glazed brick fragments from Babylon'
        ),
        'title': 'Curatorial Photograph'
    },
    '54': {
        'original_title': (
            "Reconstructing a brick with cuneiform writing from fragments "
            "excavated at Babylon"
        ),
        'title': 'Curatorial Photograph'
    },
    '55': {
        'original_title': 'Brick stamp with cuneiform inscription of a king',
        'title': 'Inscribed Brick Stamp'
    },
    '56': {
        'original_title': (
            "Brick stamped with cuneiform inscription of Nebuchadnezzar II "
            "and alphabetic worker's inscription (nbwn'd)"
        ),
        'title': 'Stamped Brick'
    },
    '57': {
        'original_title': 'Fragmentary plaque with a striding lion',
        'title': 'Ceramic Plaque'
    },
    '58': {
        'original_title': 'Plaque with a striding mušhuššu-dragon',
        'title': 'Ceramic Plaque'
    },
    '59': {
        'original_title': 'Mold for a female figurine and modern cast',
        'title': 'Mold'
    },
    '6': {
        'original_title': 'Reconstructed brick with cuneiform sign bi',
        'title': 'Reconstructed Brick'
    },
    '65': {
        'original_title': (
            "Fragmentary cuneiform tablet with a list of minerals, plants, "
            "animals, and other substances, with corresponding deities"
        ),
        'title': 'Cuneiform Tablet',
        'full_title': 'Fragmentary Cuneiform Tablet Containing a List',
        'title_detail': 'original_title'
    },
    '70': {
        'original_title': 'Three reconstructed necklaces',
        'title': 'Reconstructed Necklaces'
    },
    '71': {
        'original_title': 'Fragments of inscribed ritual axes',
        'title': 'Inscribed Axes'
    },
    '72': {
        'original_title': (
            "Stamp seal and modern impression with a worshipper or priest "
            "before the divine symbols of Marduk (spade) and Nabu (stylus)"
        ),
        'title': 'Stamp Seal',
        'full_title': 'Stamp Seal and Modern Impression',
        'title_detail': 'original_title'
    },
    '73': {
        'original_title': "Head of a composite statuette of a worshipper",
        'title': 'Head of Statuette'
    },
    '74': {
        'original_title': 'Fragmentary beard inlay from a composite statuette',
        'title': 'Statuette Inlay'
    },
    '75': {
        'original_title': (
            "Pierced eyestone with cuneiform inscription (the name of the "
            "goddess Ninlil)"
        ),
        'title': 'Inscribed Eyestone'
    },
    '77': {
        'original_title': (
            "Uncarved cylinder seal, possibly a foundation deposit"
        ),
        'title': 'Uncarved Cylinder Seal'
    },
    '78': {
        'original_title': (
            "Cylinder seal and modern impression with contest scenes between "
            "a divine hero and a bull, and between a divine hero and a lion"
        ),
        'title': 'Cylinder Seal',
        'full_title': 'Cylinder Seal and Modern Impression',
        'title_detail': 'original_title'
    },
    '79': {
        'original_title': (
            "Stamp seal in the shape of a lion and modern impression, with "
            "three animals on the seal face"
        ),
        'title': 'Stamp Seal',
        'full_title': 'Stamp Seal and Modern Impression',
        'title_detail': 'original_title'
    },
    '8': {
        'original_title': (
            "Brick fragment with mušhuššu-dragon scales"
        ),
        'title': 'Brick'
    },
    '9': {
        'original_title': (
            "Brick with fitters' marks and cuneiform inscription on reverse"
        ),
        'title': 'Brick'
    },
    '95': {
        'original_title': (
            "Reconstructed panel of bricks with a striding lion"
        ),
        'title': 'Reconstructed Brick Panel'
    },
    '96': {
        'original_title': 'Brick with guilloche motif',
        'title': 'Brick'
    },
    '97': {
        'original_title': 'Brick fragment with part of a rosette',
        'title': 'Brick'
    },
    '98': {
        'original_title': 'Three fragmentary bricks with palmette motif',
        'title': 'Bricks'
    },
    '99': {
        'original_title': 'Vessel with frieze of kneeling bulls',
        'title': 'Vessel with Bulls'
    }
}

SLUG_FIXUPS = {
    '10': 'brick-floral-1',
    '101': 'amulet-lion',
    '102': 'stamp-seal-spade-stylus',
    '103': 'brick-mold',
    '104': 'illustration-lion-fur',
    '105': 'illustration-facade-throne-room',
    '106': 'illustration-wall',
    '107': 'illustration-wall-rosette',
    '108': 'illustration-mushussu-2',
    '109': 'illustration-facade-gate',
    '11': 'brick-reed-dog',
    '110': 'illustration-gate',
    '111': 'eyestone-nebuchadnezzar-ii',
    '112': 'cylinder-seal-winged-gate',
    '113': 'cylinder-seal-lion-bull',
    '114': 'cylinder-seal-hero-lion',
    '115': 'cylinder-seal-spade-stylus',
    '116': 'cylinder-seal-king-lions',
    '117': 'bricks-bull-man',
    '118': 'brick-queen-hand',
    '119': 'brick-inscribed-2',
    '12': 'brick-nebuchadnezzar-ii-1',
    '120': 'tile-genie',
    '121': 'tile-checkerboard',
    '122': 'bricks-archer',
    '123': 'mold-female-figurine-3',
    '125': 'stela-ashurbanipal',
    '126': 'brick-nebuchadnezzar-ii-2',
    '127': 'brick-genie',
    '128': 'tablet-glass-recipe-red',
    '129': 'tablet-glass-recipes',
    '13': 'brick-lion-1',
    '131': 'cylinder-seal-enki',
    '132': 'cylinder-seal-ishtar',
    '133': 'cylinder-seal-sin-spade',
    '14': 'brick-worker-1',
    '15': 'brick-worker-2',
    '16': 'brick-water-goddess-1',
    '17': 'brick-water-goddess-2',
    '18': 'brick-mountain-god-1',
    '19': 'brick-mountain-god-2',
    '2': 'brick-fragment',
    '20': 'wall-tile-palmette',
    '21': 'brick-god-face',
    '22': 'brick-floral-2',
    '23': 'brick-rosette-1',
    '24': 'brick-rosette-2',
    '25': 'brick-rosette-3',
    '26': 'vessel-caprids',
    '27': 'vessel-clay',
    '28': 'mold-female-figurine-1',
    '29': 'figurine-apkallu',
    '3': 'brick-bull-belly',
    '30': 'necklace-stone-1',
    '31': 'cylinder-seal-hero-bull',
    '32': 'ingot-egyptian-blue',
    '33': 'ingot-glass',
    '34': 'inlay-statuette-a',
    '35': 'inlay-statuette-b',
    '36': 'inlay-statuette-c',
    '37': 'inlay-statuette-d',
    '38': 'inlay-statue-a',
    '39': 'inlay-statue-b',
    '4': 'brick-mushussu-1',
    '40': 'cylinder-seal-marduk',
    '41': 'uncarved-1',
    '42': 'uncarved-2',
    '43': 'eyestone-agate-1',
    '44': 'relief',
    '45': 'illustration-mushussu-1',
    '46': 'illustration-bull',
    '47': 'photo-beginning',
    '48': 'photo-wall-bull',
    '49': 'photo-wall-mushussu',
    '50': 'photo-unglazed-1',
    '5': 'brick-bi-1',
    '51': 'photo-unglazed-2',
    '52': 'photo-desalinating',
    '53': 'photo-sorting',
    '54': 'photo-reconstructing',
    '55': 'brick-stamp-king',
    '56': 'brick-stamp-nebuchadnezzar-ii',
    '57': 'plaque-lion',
    '58': 'plaque-mushussu',
    '59': 'mold-female-figurine-2',
    '6': 'brick-bi-2',
    '61': 'male-figurine',
    '62': 'deity-figurine',
    '63': 'figurine-lion',
    '64': 'figurine-bull',
    '65': 'tablet-lists',
    '66': 'necklace-eyestones-1',
    '67': 'necklace-eyestones-2',
    '68': 'necklace-stone-2',
    '69': 'necklace-stone-3',
    '7': 'brick-blue',
    '70': 'necklaces',
    '71': 'axes',
    '72': 'stamp-seal-vitreous',
    '73': 'statuette-worshipper',
    '74': 'inlay-statuette-e',
    '75': 'eyestone-agate-inscribed',
    '76': 'eyestone-agate-2',
    '77': 'uncarved-3',
    '78': 'cylinder-seal-contests',
    '79': 'stamp-seal-lion',
    '8': 'brick-mushussu-2',
    '80': 'amulet-bull',
    '81': 'bull-head',
    '82': 'bottle-cosmetic',
    '83': 'vessel-glass',
    '84': 'vessel-perfume-1',
    '85': 'vessel-perfume-2',
    '86': 'ornament',
    '87': 'cullet-1',
    '88': 'cullet-2',
    '89': 'cullet-3',
    '9': 'brick-inscribed-1',
    '90': 'cullet-4',
    '91': 'cullet-5',
    '92': 'beads',
    '93': 'bead-maker',
    '95': 'brick-lion-2',
    '96': 'brick-guilloche',
    '97': 'brick-rosette-4',
    '98': 'brick-palmette'
}


class IshtarCollection(ObjectCollection):

    def __init__(self, crosswalk=ISHTAR_CROSSWALK):
        ObjectCollection.__init__(self, crosswalk=crosswalk)

    def fix_titles(self):
        for obj_id, obj in self.objects.items():
            try:
                title_fixup = TITLE_FIXUPS[obj_id]
            except KeyError:
                pass
            else:
                if obj.data['title'] == title_fixup['original_title']:
                    fixup_keys = ['title', 'full_title', 'title_detail']
                    for fixup_key in fixup_keys:
                        try:
                            fu = title_fixup[fixup_key]
                        except KeyError:
                            pass
                        else:
                            if fu in fixup_keys + ['original_title']:
                                fu = title_fixup[fu]
                            obj.data[fixup_key] = fu
                    if obj.data['full_title'] is None and \
                       obj.data['title'] != title_fixup['original_title']:
                        obj.data['full_title'] = title_fixup['original_title']
                else:
                    logger.error(
                        'Title/ID drift for ID = "{}". Expected "{}". Got "{}"'
                        ''.format(
                            obj_id,
                            title_fixup['original_title'],
                            obj.data['title'])
                    )

    def _set_slug(self, obj_id):
        try:
            slug = SLUG_FIXUPS[obj_id]
        except KeyError:
            slug = None
        return slug
