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


class MonthsWidget(Gtk.Box):
    """docstring for MonthsWidget"""
    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL)
        # self.destroy()
        # self.setup_years()
        self.setup_grid()

    def setup_grid(self):
        self.frame = Gtk.Frame()
        self.grid = Gtk.Grid()
        self.frame.add(self.grid)
        self.pack_start(self.frame, False, True, 0)
        self.grid.set_column_homogeneous(True)
        self.grid.set_column_spacing(spacing=10)
        self.grid.set_row_homogeneous(True)
        self.grid.set_row_spacing(spacing=10)
        self.grid.button_list = []
        for i, month in enumerate(self.get_months()):
            button = Gtk.Button(label=month)
            if i+1 == self.date.month:
                button.set_relief(Gtk.ReliefStyle.HALF)
                self.grid.set_focus_child(button)
                # button.grab_focus()
            else:
                button.set_relief(Gtk.ReliefStyle.NONE)
            if self.rtl:
                self.grid.attach(button, 2 - i % 3, i // 3, 1, 1)
            else:
                self.grid.attach(button, i % 3, i // 3, 1, 1)
            self.grid.button_list.append((button, month, i+1))


class PersianMonthsWidget(MonthsWidget, PersianCalendar):
    """docstring for PersianMonthsWidget"""
    def __init__(self, date=None, rtl=True):
        PersianCalendar.__init__(self, date)
        self.rtl = rtl
        MonthsWidget.__init__(self)


class GeorgianMonthsWidget(MonthsWidget, GeorgianCalendar):
    """docstring for GeorgianMonthsWidget"""
    def __init__(self, date=None, rtl=False):
        GeorgianCalendar.__init__(self, date)
        self.rtl = rtl
        MonthsWidget.__init__(self)
