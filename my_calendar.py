#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2014    Amir Mohammadi <183.amir@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.    See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

from calendar import Calendar, monthrange
import datetime
import khayyam
import calendar

from jalali_date_persian_numbers import JalaliDatePersianNumbers


def add_years(date, years):
    return date.replace(year=date.year+years)


def date_to_georgian(date):
    if isinstance(date, khayyam.JalaliDate):
        return date.to_date()
    return date


def add_one_month(t):
    """Return a `datetime.date` or `datetime.datetime` (as given) that is
    one month earlier.

    Note that the resultant day of the month might change if the following
    month has fewer days:

        >>> add_one_month(datetime.date(2010, 1, 31))
        datetime.date(2010, 2, 28)
    """
    import datetime
    one_day = datetime.timedelta(days=1)
    one_month_later = t + one_day
    while one_month_later.month == t.month:  # advance to start of next month
        one_month_later += one_day
    target_month = one_month_later.month
    while one_month_later.day < t.day:  # advance to appropriate day
        one_month_later += one_day
        if one_month_later.month != target_month:  # gone too far
            one_month_later -= one_day
            break
    return one_month_later


def subtract_one_month(t):
    """Return a `datetime.date` or `datetime.datetime` (as given) that is
    one month later.

    Note that the resultant day of the month might change if the following
    month has fewer days:

        >>> subtract_one_month(datetime.date(2010, 3, 31))
        datetime.date(2010, 2, 28)
    """
    import datetime
    one_day = datetime.timedelta(days=1)
    one_month_earlier = t - one_day
    while one_month_earlier.month == t.month or one_month_earlier.day > t.day:
        one_month_earlier -= one_day
    return one_month_earlier


def add_months(date, months):
    '''http://code.activestate.com/recipes/
    577274-subtract-or-add-a-month-to-a-datetimedate-or-datet/
    Note: months may be positive, or negative, but must be an integer.
    If favorEoM (favor End of Month) is true and input date is the last day
    of the month then return an offset date that also falls on the last day
    of the month.'''
    if months == 0:
        return date
    elif months > 0:
        for _ in range(months):
            date = add_one_month(date)
    else:
        for _ in range(abs(months)):
            date = subtract_one_month(date)
    return date


class MyCalendar(Calendar):
    """docstring for MyCalendar"""
    def get_first_day_month(self):
        first_day_of_month = self.date+datetime.timedelta(days=1-self.date.day)
        first_day_of_month = first_day_of_month.weekday()
        first_day_of_month = (first_day_of_month+self.first_week_day_offset) % 7
        # print('first_day_of_month', first_day_of_month)
        return first_day_of_month

    def gen_grid_mat(self):

        # decide if it is going to be 6 rows or 5
        if self.first_day_of_month + self.days_in_month > 35:
            rows = 6
        else:
            rows = 5

        self.grid_mat = []  # 5 or 6 row, 7 column
        for _ in range(rows):
            row = []
            for _ in range(7):
                row.append([])
            self.grid_mat.append(row)
        delta = - (self.first_day_of_month + self.date.day) + 1
        # print(delta)
        for j in range(rows):
            for i in range(7):
                if self.rtl:
                    delta_time = datetime.timedelta(days=6-i+j*7+delta)
                else:
                    delta_time = datetime.timedelta(days=i+j*7+delta)
                date = self.date+delta_time
                if date.month == self.date.month:
                    text = '<span fgcolor="black">{}</span>'
                else:
                    text = '<span fgcolor="gray">{}</span>'
                self.grid_mat[j][i] = (date, text.format(date.strftime('%d')))


class PersianCalendar(MyCalendar):
    """docstring for PersianCalendar"""
    def __init__(self, date=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # khayyam.JalaliDate.__init__(self)
        if date is None:
            date = khayyam.JalaliDate.today()
        date = khayyam.JalaliDate.from_date(date_to_georgian(date))
        date = JalaliDatePersianNumbers(date.year, date.month, date.day)
        # print(date, date.strftime('%d'))
        self.date = date
        self.days_in_month = self.date.days_in_month
        self.first_week_day_offset = 2
        self.first_day_of_month = self.get_first_day_month()

    def get_week_days(self):
        return [('ش', 'شنبه'), ('۱ش', 'یک‌شنبه'), ('۲ش', 'دو‌شنبه'),
                ('۳ش', 'سه‌شنبه'), ('۴ش', 'چهار‌شنبه'),
                ('۵ش', 'پنج‌شنبه'), ('آ', 'آدینه')]

    def get_months(self):
        return khayyam.jalali_date.PERSIAN_MONTH_NAMES.values()


class GeorgianCalendar(MyCalendar):
    """docstring for GeorgianCalendar"""
    def __init__(self, date=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # datetime.datetime.__init__(self)
        if date is None:
            date = datetime.date.today()
        self.date = date_to_georgian(date)
        self.days_in_month = monthrange(self.date.year, self.date.month)[1]
        # print('self.days_in_month', self.days_in_month)
        self.first_week_day_offset = 0
        self.first_day_of_month = self.get_first_day_month()

    def get_week_days(self):
        return [('Mon', 'Monday'), ('Tue', 'Tuesday'), ('Wed', 'Wednesday'),
                ('Thu', 'Thursday'), ('Fri', 'Friday'), ('Sat', 'Saturday'),
                ('Sun', 'Sunday')]

    def get_months(self):
        return calendar.month_name[1:]

if __name__ == '__main__':
    pass
