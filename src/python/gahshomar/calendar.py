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

import logging
logger = logging.getLogger(__name__)
import calendar
from calendar import Calendar, monthrange
import datetime
from gi.repository import GLib
from gettext import gettext as _

import gahshomar.khayyam as khayyam
from . import log


@log
def glib_strftime(frm, odate):
    if isinstance(odate, datetime.date):
        date = GLib.DateTime.new_local(odate.year, odate.month, odate.day,
                                       0, 0, 0)
        return date.format(_(frm))
    else:
        return odate.strftime(frm.replace('O', ''))

@log
def add_years(date, years):
    while True:
        try:
            return date.replace(year=date.year+years)
        except ValueError:
            date -= datetime.timedelta(days=1)


@log
def date_to_georgian(date):
    if isinstance(date, khayyam.JalaliDate):
        return date.to_date()
    return date


@log
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


@log
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


@log
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
        for __ in range(months):
            date = add_one_month(date)
    else:
        for __ in range(abs(months)):
            date = subtract_one_month(date)
    return date


class MyCalendar(Calendar):
    """docstring for MyCalendar"""
    @log
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @log
    def get_first_day_month(self):
        first_day_of_month = self.date+datetime.timedelta(days=1-self.date.day)
        first_day_of_month = first_day_of_month.weekday()
        first_day_of_month = (first_day_of_month) % 7
        # print('first_day_of_month', first_day_of_month)
        return first_day_of_month

    @log
    def gen_grid_mat(self):

        # decide if it is going to be 6 rows or 5
        if self.get_first_day_month() + self.get_days_in_month() > 35:
            rows = 6
        else:
            rows = 5

        self.grid_mat = []  # 5 or 6 row, 7 column
        for __ in range(rows):
            row = []
            for __ in range(7):
                row.append([])
            self.grid_mat.append(row)
        delta = - (self.get_first_day_month() + self.date.day) + 1
        # print(delta)
        for j in range(rows):
            for i in range(7):
                if self.rtl:
                    delta_time = datetime.timedelta(days=6-i+j*7+delta)
                else:
                    delta_time = datetime.timedelta(days=i+j*7+delta)
                date = self.date+delta_time
                # if date.month == self.date.month:
                #     text = '<span fgcolor="black">{}</span>'
                # else:
                #     text = '<span fgcolor="gray">{}</span>'
                text = '{}'
                d = glib_strftime(_('%d'), date)
                if d[0] == '0' or d[0] == '۰':
                    d = d[1:]
                self.grid_mat[j][i] = (date, text.format(d))


class PersianCalendar(MyCalendar):
    """docstring for PersianCalendar"""
    @log
    def __init__(self, date=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # khayyam.JalaliDate.__init__(self)
        if date is None:
            date = khayyam.JalaliDate.today()
        date = self.get_date(date)
        self.date = date
        self.first_week_day_offset = 2

    @log
    def get_days_in_month(self):
        return self.date.days_in_month

    @log
    def get_date(self, date):
        date = khayyam.JalaliDate.from_date(date_to_georgian(date))
        return date

    @log
    def get_week_days(self):
        return [(_('ش'), _('شنبه')), (_('۱ش'), _('یک‌شنبه')),
                (_('۲ش'), _('دو‌شنبه')), (_('۳ش'), _('سه‌شنبه')),
                (_('۴ش'), _('چهار‌شنبه')), (_('۵ش'), _('پنج‌شنبه')),
                (_('آ'), _('آدینه'))]

    @log
    def get_months(self):
        return list(khayyam.jalali_date.PERSIAN_MONTH_NAMES.values())


class GeorgianCalendar(MyCalendar):
    """docstring for GeorgianCalendar"""
    @log
    def __init__(self, date=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # datetime.datetime.__init__(self)
        if date is None:
            date = datetime.date.today()
        self.date = self.get_date(date)
        # print('self.days_in_month', self.days_in_month)
        self.first_week_day_offset = 0

    @log
    def get_days_in_month(self):
        return monthrange(self.date.year, self.date.month)[1]

    @log
    def get_date(self, date):
        return date_to_georgian(date)

    @log
    def get_week_days(self):
        return [(_('Mon'), _('Monday')), (_('Tue'), _('Tuesday')),
                (_('Wed'), _('Wednesday')), (_('Thu'), _('Thursday')),
                (_('Fri'), _('Friday')), (_('Sat'), _('Saturday')),
                (_('Sun'), _('Sunday'))]

    @log
    def get_months(self):
        return list(calendar.month_name[1:])
