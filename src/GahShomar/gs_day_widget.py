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

from gi.repository import Gtk
from .gs_calendar import PersianCalendar, GeorgianCalendar


class DayWidget(Gtk.Box):
    """docstring for DayWidget"""
    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL)
        # self.destroy()
        # self.setup_big_day()
        self.setup_date()

    def setup_big_day(self):
        self.big_day2 = Gtk.Label()
        self.pack_start(self.big_day2, True, True, 10)
        text = self.date.strftime('%d')
        self.big_day2.set_markup("<span size='xx-large'>"+text+'</span>')

    def setup_date(self):
        self.big_day = Gtk.Label()
        self.pack_start(self.big_day, True, True, 10)
        text = self.date.strftime(self.date_format)
        self.big_day.set_markup("<span size='large'>"+text+'</span>')


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
