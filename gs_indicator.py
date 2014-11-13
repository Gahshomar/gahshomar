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

import datetime
from gi.repository import Gtk, GObject
import khayyam
try:
    from gi.repository import AppIndicator3 as AppIndicator
    USE_IND = True
except ImportError:
    USE_IND = False


class GahShomarIndicator(GObject.GObject):
    def __init__(self, parent, date=None):
        super().__init__()
        if not USE_IND:
            return
        if date is None:
            date = datetime.date.today()
        self.date = date
        self.parent = parent
        self.base_folder = self.parent.full_path
        self.icon_name = parent.config['Global']['icon_name']
        # self.icon_folder = parent.config['AppIndicator']['default_icon_folder']
        cats = 'cat = AppIndicator.IndicatorCategory.{}'
        cats = cats.format(parent.config['AppIndicator']['indicator_category'])
        d = locals()
        exec(cats, globals(), d)
        cat = d['cat']
        self.ind = AppIndicator.Indicator.new(
            "GahShomar-indicator",
            self.icon_name.format(day=self.date.day),
            cat)
        self.ind.set_status(AppIndicator.IndicatorStatus.ACTIVE)

        self.menu_setup()
        self.ind.set_menu(self.menu)
        self.update()

    def menu_setup(self):
        self.menu = Gtk.Menu()
        self.menu.set_halign(Gtk.Align.CENTER)

        self.today_item = Gtk.MenuItem('امروز')
        self.today_item.set_right_justified(True)
        self.today_item.show()
        self.today_item.set_halign(Gtk.Align.CENTER)
        label = self.today_item.get_children()[0]
        label.set_halign(Gtk.Align.CENTER)

        self.toggle_main_window = Gtk.MenuItem("گاه‌شمار")
        self.toggle_main_window.set_right_justified(True)
        self.toggle_main_window.connect("activate", self.parent.toggle_main_win)
        self.toggle_main_window.show()
        self.toggle_main_window.set_halign(Gtk.Align.CENTER)
        self.toggle_main_window.set_state_flags(Gtk.StateFlags.DIR_RTL, False)
        label = self.toggle_main_window.get_children()[0]
        label.set_halign(Gtk.Align.CENTER)
        label.set_state_flags(Gtk.StateFlags.DIR_RTL, False)

        self.quit_item = Gtk.MenuItem("خروج")
        self.quit_item.set_right_justified(True)
        self.quit_item.connect("activate", self.quit)
        self.quit_item.show()
        self.quit_item.set_halign(Gtk.Align.CENTER)
        label = self.quit_item.get_children()[0]
        label.set_halign(Gtk.Align.CENTER)

        self.menu.append(self.today_item)
        self.menu.append(self.toggle_main_window)
        self.menu.append(self.quit_item)

    def get_date(self, date, frmt=None):
        if frmt is None:
            frmt = self.parent.config['AppIndicator']['date_format']
        return khayyam.JalaliDate.from_date(date).strftime(frmt)

    def quit(self, widget):
        self.parent.app.quit()

    def update(self):
        if not USE_IND:
            return
        self.date = datetime.date.today()
        self.today_item.set_label(self.get_date(self.date))
        self.set_icon()

    def set_icon(self):
        # self.ind.set_icon_theme_path(
        #     os.path.join(self.base_folder, self.icon_folder))
        self.ind.set_icon(self.icon_name.format(
            day=khayyam.JalaliDate.from_date(self.date).day))
