# -*- coding: utf-8 -*-

import re
from .compat import get_unicode
from .constants import NUM_DICT, INV_NUM_DICT

__author__ = 'vahid'


def latinN2PersianN(num):
    numP = ''
    for v in num:
        if v in NUM_DICT:
            numP += NUM_DICT[v]
        else:
            numP += v
    return numP


def PersianN2latinN(num):
    numP = ''
    for v in num:
        if v in INV_NUM_DICT:
            numP += INV_NUM_DICT[v]
        else:
            numP += v
    return numP


def replace_if_match(data, pattern, new):
    if re.search(pattern, data):
        if hasattr(new, '__call__'):
            new = new()
        return data.replace(pattern, latinN2PersianN(get_unicode(new)))
    return data
