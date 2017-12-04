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
import calendar
import datetime
from gi.repository import GLib, Gio, GObject
from gettext import gettext as _

import gahshomar.khayyam as khayyam
logger = logging.getLogger(__name__)


def glib_strftime(frm, odate):
    if isinstance(odate, datetime.date):
        date = GLib.DateTime.new_local(odate.year, odate.month, odate.day,
                                       0, 0, 0)
        return date.format(_(frm))
    else:
        return odate.strftime(frm.replace('O', ''))


def add_years(date, years):
    while True:
        try:
            return date.replace(year=date.year + years)
        except ValueError:
            date -= datetime.timedelta(days=1)


def date_to_georgian(date):
    if isinstance(date, khayyam.JalaliDate):
        return date.to_date()
    return date


def date_to_jalali(date):
    if isinstance(date, khayyam.JalaliDate):
        return date
    return khayyam.JalaliDate.from_date(date)


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
    '''
    if months == 0:
        return date
    elif months > 0:
        for __ in range(months):
            date = add_one_month(date)
    else:
        for __ in range(abs(months)):
            date = subtract_one_month(date)
    return date


class Date(GObject.GObject):
    """The class for representing dates in Gahshomar
    """

    def __init__(self, date=None, **kwargs):
        self._date = date
        super().__init__(**kwargs)

    @GObject.Property
    def date(self):
        return self._date

    @date.setter
    def date(self, value):
        self._date = self.to_correct_date(value)

    @property
    def first_day_month(self):
        first_day_of_month = self.date + \
            datetime.timedelta(days=1 - self.date.day)
        first_day_of_month = first_day_of_month.weekday()
        first_day_of_month = (first_day_of_month) % 7
        return first_day_of_month

    @property
    def grid_mat(self):

        # decide if it is going to be 6 rows or 5
        if self.first_day_month + self.days_in_month > 35:
            rows = 6
        else:
            rows = 5

        grid_mat = []  # 5 or 6 row, 7 column
        for __ in range(rows):
            row = []
            for __ in range(7):
                row.append([])
            grid_mat.append(row)
        delta = - (self.first_day_month + self.date.day) + 1
        for j in range(rows):
            for i in range(7):
                if self.rtl:
                    delta_time = datetime.timedelta(days=6 - i + j * 7 + delta)
                else:
                    delta_time = datetime.timedelta(days=i + j * 7 + delta)
                date = self.date + delta_time
                text = '{}'
                d = glib_strftime(_('%d'), date)
                if d[0] == '0' or d[0] == '۰':
                    d = d[1:]
                grid_mat[j][i] = (date, text.format(d))
        return grid_mat

    @property
    def year(self):
        return self.date.year

    @property
    def month(self):
        return self.date.month

    @property
    def day(self):
        return self.date.day

    @property
    def full_date(self):
        return glib_strftime(self.date_format, self.date)

    def strftime(self, date_format):
        return glib_strftime(date_format, self.date)

    def today(self):
        return self.to_correct_date(datetime.date.today())

    def add_months(self, n):
        return add_months(self.date, n)

    def add_years(self, n):
        return add_years(self.date, n)

    def replace(self, *args, **kwargs):
        return self.date.replace(*args, **kwargs)

    def on_date_changed(self, object, *args):
        self.date = object.date

    def on_update_to_today(self, *args):
        self.date = self.today()
        # return True so the timeout keeps continuing
        return True


class GeorgianDate(Date):

    def __init__(self, date=None, *args, **kwargs):
        date = date_to_georgian(date or datetime.date.today())
        self.first_week_day_offset = 0
        self.rtl = False
        settings = Gio.Settings.new('org.gnome.Gahshomar')
        self.date_format = str(settings.get_value('georgian-date-format'))
        self.date_format = self.date_format.replace("'", "")
        super().__init__(date, *args, **kwargs)

    @property
    def days_in_month(self):
        return calendar.monthrange(self.date.year, self.date.month)[1]

    @property
    def week_days(self):
        return [(_('Mon'), _('Monday')), (_('Tue'), _('Tuesday')),
                (_('Wed'), _('Wednesday')), (_('Thu'), _('Thursday')),
                (_('Fri'), _('Friday')), (_('Sat'), _('Saturday')),
                (_('Sun'), _('Sunday'))]

    @property
    def months(self):
        return list(calendar.month_name[1:])

    def to_correct_date(self, date):
        return date_to_georgian(date)


class PersianDate(Date):

    def __init__(self, date=None, *args, **kwargs):
        date = date_to_jalali(date or datetime.date.today())
        self.first_week_day_offset = 2
        self.rtl = True
        settings = Gio.Settings.new('org.gnome.Gahshomar')
        if bool(settings.get_value('afghan-month')):
            self.date_format = str(settings.get_value('afghan-date-format'))
        else:
            self.date_format = str(settings.get_value('persian-date-format'))
        self.date_format = self.date_format.replace("'", "")
        super().__init__(date, *args, **kwargs)

    @property
    def days_in_month(self):
        return self.date.days_in_month

    @property
    def week_days(self):
        return [(_('ش'), _('شنبه')), (_('۱ش'), _('یک‌شنبه')),
                (_('۲ش'), _('دو‌شنبه')), (_('۳ش'), _('سه‌شنبه')),
                (_('۴ش'), _('چهار‌شنبه')), (_('۵ش'), _('پنج‌شنبه')),
                (_('آ'), _('آدینه'))]

    @property
    def months(self):
        settings = Gio.Settings.new('org.gnome.Gahshomar')
        if bool(settings.get_value('afghan-month')):
            return list(khayyam.AFGHAN_MONTH_NAMES.values())
        else:
            return list(khayyam.PERSIAN_MONTH_NAMES.values())

    def to_correct_date(self, date):
        return date_to_jalali(date)


GREGORIAN_DATE = GeorgianDate()
"""This object represents the current selected Gregorian date in Gahshomar's
interface. You can connect to its signal to see if selected date has changed:
``GREGORIAN_DATE.connect("notify::date", on_date_changed)``
"""
PERSIAN_DATE = PersianDate()
"""This object represents the current selected Persian date in Gahshomar's
interface. You can connect to its signal to see if selected date has changed:
``PERSIAN_DATE.connect("notify::date", on_date_changed)``
"""
# connect the current Persian date to the current Gregorian date
GREGORIAN_DATE.connect("notify::date", PERSIAN_DATE.on_date_changed)

TODAY = GeorgianDate()
"""This object represents today in Gahshomar's interface.
You can connect to its signal to see if today has changed:
``TODAY.connect("notify::date", on_today_changed)``
"""
# update today every 10 seconds
GLib.timeout_add_seconds(priority=GLib.PRIORITY_DEFAULT,
                         interval=10, function=TODAY.on_update_to_today)
