#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Persian (Jalali/Farsi) Calendar which provides an app indicator for the Unity Desktop Environment.
# requires python 2.3 (maybe 2.7) and above
# should work on python 3 too if you have the Khayyam library available

# Copyright (C) 2014  Amir Mohammadi <183.amir@gmail.com>

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import sys
import os
import gtk
import appindicator

import khayyam

PING_FREQUENCY = 10 # In seconds; the frequency of updating the date
DATE_FORMAT = '%A, %d %B %Y' # Day of the week, day month year
ICON_NAME = "persian-calendar-dark-theme" # name of the icon file
# ICON_NAME = "persian-calendar-light-theme" # if you are using a light theme, you can use this icon

INDICATOR_CATEGORY = appindicator.CATEGORY_SYSTEM_SERVICES
# appindicator.CATEGORY_SYSTEM_SERVICES
# appindicator.CATEGORY_APPLICATION_STATUS
# appindicator.CATEGORY_COMMUNICATIONS
# appindicator.CATEGORY_HARDWARE
# appindicator.CATEGORY_OTHER



class PersianCalendar:
  def __init__(self):
    self.date = khayyam.JalaliDate.today()
    self.ind = appindicator.Indicator("persian-calendar-indicator",
                       ICON_NAME,
                       INDICATOR_CATEGORY, os.path.dirname(__file__))
    print os.path.realpath(__file__)
    self.ind.set_status(appindicator.STATUS_ACTIVE)

    self.menu_setup()
    self.ind.set_menu(self.menu)

  def menu_setup(self):
    self.menu = gtk.Menu()

    self.quit_item = gtk.MenuItem("Quit")
    self.quit_item.connect("activate", self.quit)
    self.quit_item.show()

    self.today_item = gtk.MenuItem('Today')
    self.today_item.show()

    self.menu.append(self.today_item)
    self.menu.append(self.quit_item)

  def main(self):
    self.change_time()
    gtk.timeout_add(PING_FREQUENCY * 1000, self.change_time)
    gtk.main()

  def quit(self, widget):
    sys.exit(0)

  def get_date(self, frmt=DATE_FORMAT):
    return self.date.strftime(frmt)

  def change_time(self):
    self.today_item.set_label(self.get_date())


if __name__ == "__main__":
  indicator = PersianCalendar()
  indicator.main()
