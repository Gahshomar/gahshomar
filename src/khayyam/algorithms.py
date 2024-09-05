# -*- coding: utf-8 -*-
__author__ = 'vahid'

from math import floor, ceil
from .jalaali import Jalaali


def get_julian_day_from_gregorian(year, month, day):
    return Jalaali.g2d(year, month, day)

def is_leap_year(year):
    return Jalaali.is_leap_jalaali_year(year)


def days_in_month(year, month):
    return Jalaali.jalaali_month_length(year, month)


def julian_day_from_jalali_date(year, month, day):
    return Jalaali.j2d(year, month, day)


def jalali_date_from_julian_day(julian_day):
    date = Jalaali.d2j(julian_day)
    return date["jy"], date["jm"], date["jd"]

def gregorian_date_from_julian_day(jd):
    date = Jalaali.d2g(jd)
    return date["gy"], date["gm"], date["gd"]


def jalali_date_from_gregorian_date(year, month, day):
    return jalali_date_from_julian_day(
        get_julian_day_from_gregorian(year, month, day))


def parse(cls, date_string, format, valid_codes):
    available_codes = {}
    for code in valid_codes:
        try:
            i = format.index(code)
            available_codes[i] = code
        except ValueError:
            continue

    parts = []
    for code_index in sorted(available_codes):
        code = available_codes[code_index]
        try:
            i = format.index(code)
            if i > 0:
                parts.append(('gap', format[:i]))
            parts.append(('field', code))
            format = format[i + len(code):]
        except ValueError:
            continue

    fields = {}
    field_start = None
    for part in parts:
        if part[0] == 'gap':  # Gap
            if field_start:
                gap_index = date_string.index(part[1])
                fields[field_start] = date_string[:gap_index]
                field_start = None
                date_string = date_string[gap_index + len(part[1]):]
            else:
                date_string = date_string[len(part[1]):]
        else:  # Field
            if field_start:
                fields[field_start] = date_string[:valid_codes[part[1]][0]]
            else:
                field_start = part[1]

    if field_start:
        fields[field_start] = date_string

    values = {}
    for field, value in fields.items():
        values[valid_codes[field][1]] = int(value)

    result = cls(**values)

    return result
