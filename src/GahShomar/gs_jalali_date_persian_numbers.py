#!/usr/bin/env python3
# -*- Mode: Python; coding: utf-8; indent-tabs-mode: s; tab-width: 4 -*-
#
# Copyright (C) 2014 Amir Mohammadi <183.amir@gmail.com>
#
# Gahshomar is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Gahshomar is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

import khayyam
import collections
import re

NUM_DICT = {'0': '۰',
            '1': '۱',
            '2': '۲',
            '3': '۳',
            '4': '۴',
            '5': '۵',
            '6': '۶',
            '7': '۷',
            '8': '۸',
            '9': '۹'}

INV_NUM_DICT = {v: k for k, v in NUM_DICT.items()}


def latinN2PersianN(num):
    numP = ''
    for v in num:
        if v in NUM_DICT:
            numP += NUM_DICT[v]
        else:
            numP += v
    return numP


def PersianN2latinN(num):
    return str(int(num))


def _replace_if_match(data, pattern, new):
        if re.search(pattern, data):
                if isinstance(new, collections.Callable):
                        new = new()
                if not isinstance(new, str):
                        new = str(new)
                return data.replace(pattern, latinN2PersianN(new))
        return data


class JalaliDatePersianNumbers(khayyam.JalaliDate):
    """JalaliDate class with Persian numbers"""

    def strftime(self, frmt):
        """
=========        =======
Directive        Meaning
=========        =======
%a                     Locale’s abbreviated weekday name.
%A                     Locale’s full weekday name.
%b                     Locale’s abbreviated month name.
%B                     Locale’s full month name.
%d                     Day of the month as a decimal number [01,31].
%j                     Day of the year as a decimal number [001,366].
%m                     Month as a decimal number [01,12].
%U                     Week number of the year (Sunday as the first day of the
 week) as a decimal number [00,53]. All days in a new year preceding the first
  Sunday are considered to be in week 0.        (4)
%w                     Weekday as a decimal number [0(Sunday),6].
%W                     Week number of the year (Monday as the first day of the
 week) as a decimal number [00,53]. All days in a new year preceding the first
  Monday are considered to be in week 0.        (4)
%x                     Locale’s appropriate date representation.
%y                     Year without century as a decimal number [00,99].
%Y                     Year with century as a decimal number.
%%                     A literal '%' character.
=========        =======
        """
        result = _replace_if_match(frmt,     '%Y', self.year)
        result = _replace_if_match(result, '%y', lambda: str(self.year)[-2:])
        result = _replace_if_match(result, '%m', self.month)
        result = _replace_if_match(result, '%d', self.day)
        result = _replace_if_match(result, '%a', self.weekdayabbr)
        result = _replace_if_match(result, '%A', self.weekdayname)
        result = _replace_if_match(result, '%b', self.monthabbr)
        result = _replace_if_match(result, '%B', self.monthname)
        result = _replace_if_match(result, '%x', self.localformat)
        result = _replace_if_match(result, '%j', self.dayofyear)
        result = _replace_if_match(result, '%U', lambda: self.weekofyear(6))
        result = _replace_if_match(result, '%W', lambda: self.weekofyear(0))
        result = _replace_if_match(result, '%w', self.weekday)
        result = _replace_if_match(result, '%%', '%')
        return result

    def __add__(self, x):
        d = super().__add__(x)
        return JalaliDatePersianNumbers(d.year, d.month, d.day)


if __name__ == '__main__':
    pass
