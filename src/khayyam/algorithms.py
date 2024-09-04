# -*- coding: utf-8 -*-
__author__ = 'vahid'

from math import floor, ceil


def get_julian_day_from_gregorian(year, month, day):
    # Checking #
    if year / 4.0 == round(year / 4.0):
        if year / 100.0 == round(year / 100.0):
            if year / 400.0 == round(year / 400.0):
                # Leap year checking #
                if month == 2:
                    assert day <= 29, 'Invalid date'
        else:
            # Leap year #
            if month == 2:
                assert day <= 29, 'Invalid date'

    y = year + 0.0
    m = month + 0.0
    d = day + 0.0

    # Determine JD
    if m <= 2:
        y -= 1
        m += 12

    a = floor(y / 100)
    return floor(365.25 * (y + 4716)) + floor(
        30.6001 * (m + 1)) + d + (2 - a + floor(a / 4)) - 1524.5

LEAP_REMINDERS = [1, 5, 9, 13, 17, 22, 26, 30]

def is_leap_year(year):
    remainder = year - (year // 33) * 33
    return remainder in LEAP_REMINDERS


def days_in_month(year, month):
    if 1 <= month <= 6:
        return 31
    elif 7 <= month < 12:
        return 30

    assert month == 12, 'Month must be between 1 and 12'

    ### Esfand(اسفند) ###
    if is_leap_year(year):
        return 30  #Leap Year
    else:
        return 29


def julian_day_from_jalali_date(year, month, day):
    base = year - ([473, 474][year >= 0])
    julian_year = 474 + (base % 2820)
    return day + ([
        ((month - 1) * 30) + 6, (month - 1) * 31
    ][month <= 7]) + floor(((julian_year * 682) - 110) / 2816) + (
        julian_year - 1) * 365 + floor(base / 2820) * 1029983 + (1948320.5 - 1)


def jalali_date_from_julian_day(julian_day):
    julian_day = floor(julian_day) + 0.5
    offset = julian_day - 2121445.5  # julian_day_from_jalali(475, 1, 1) replaced by its static value
    cycle = floor(offset / 1029983)
    remaining = offset % 1029983
    if remaining == 1029982:
        year_cycle = 2820
    else:
        a1 = floor(remaining / 366)
        a2 = remaining % 366
        year_cycle = floor(
            ((2134 * a1) + (2816 * a2) + 2815) / 1028522) + a1 + 1
    y = year_cycle + (2820 * cycle) + 474
    if y <= 0:
        y -= 1
    days_in_years = (julian_day - julian_day_from_jalali_date(y, 1, 1)) + 1
    m = ceil([(days_in_years - 6) / 30,
              days_in_years / 31][days_in_years <= 186])
    day = (julian_day - julian_day_from_jalali_date(y, m, 1)) + 1
    return y, m, day


def gregorian_date_from_julian_day(jd):
    y = 0
    m = 0

    if jd <= 0.0:
        raise ValueError('Invalid Date')

    jdm = jd + 0.5
    z = floor(jdm)
    f = jdm - z

    alpha = floor((z - 1867216.25) / 36524.25)
    b = (z + 1 + alpha - floor(alpha / 4)) + 1524
    c = floor((b - 122.1) / 365.25)
    d = floor(365.25 * c)
    e = floor((b - d) / 30.6001)
    day = b - d - floor(30.6001 * e) + f

    if e < 14:
        m = e - 1
    elif e == 14 or e == 15:
        m = e - 13

    if m > 2:
        y = c - 4716
    elif m == 1 or m == 2:
        y = c - 4715

    return y, m, day


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
