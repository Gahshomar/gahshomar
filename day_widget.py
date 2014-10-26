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

from gi.repository import Gtk
from my_calendar import PersianCalendar, GeorgianCalendar


class DayWidget(Gtk.Box):
    """docstring for DayWidget"""
    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL)
        # self.destroy()
        self.setup_big_day()
        self.setup_date()

    def setup_big_day(self):
        day = Gtk.Label()
        self.pack_start(day, True, True, 10)
        text = self.date.strftime('%d')
        day.set_markup("<span size='xx-large'>"+text+'</span>')

    def setup_date(self):
        day = Gtk.Label()
        self.pack_start(day, True, True, 10)
        text = self.date.strftime(self.date_format)
        day.set_markup("<span size='large'>"+text+'</span>')


class PersianDayWidget(DayWidget, PersianCalendar):
    """docstring for PersianDayWidget"""
    def __init__(self, date=None):
        PersianCalendar.__init__(self, date)
        self.date_format = '%A، %d %B %Y'
        DayWidget.__init__(self)


class GeorgianDayWidget(DayWidget, GeorgianCalendar):
    """docstring for GeorgianDayWidget"""
    def __init__(self, date=None):
        GeorgianCalendar.__init__(self, date)
        self.date_format = '%A, %d %B %Y'
        DayWidget.__init__(self)
