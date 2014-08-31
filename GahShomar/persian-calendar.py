#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Persian (Jalali/Farsi) Calendar which provides an app indicator.
# requires python 2.3 (it has been tested on 2.7 only) and 
# above but not python 3.

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
import re
# import gtk
# import appindicator
from pprint import pprint


default_settings = {# do not modify this, modify ~/.config/persian-calendar/settings
'PING_FREQUENCY' : 3, # In seconds; the frequency of updating the date
'DATE_FORMAT' : '%A، %d %B %Y', # Day of the week, day month year
'ICON_NAME' : "persian-calendar-{day}", # name of the icon file
'ICON_FOLDER_DARK' : "data/icons/ubuntu-mono-dark", # name of the icon file
'ICON_FOLDER_LIGHT' : "data/icons/ubuntu-mono-light", # if you are using a light theme, you can use this icon
'DEFAULT_ICON_FOLDER' : 'data/icons/ubuntu-mono-dark',
'DEBUG': False,

'INDICATOR_CATEGORY' : 'HARDWARE',
# SYSTEM_SERVICES
# APPLICATION_STATUS
# COMMUNICATIONS
# HARDWARE
# OTHER
}
CONFIG_FILE_PATH = os.path.join(os.path.expanduser("~"), '.config', 'persian-calendar', 'settings')

# get the full path of the file
if os.path.dirname(sys.argv[0]) != ".":
    if sys.argv[0][0] == "/":
        full_path = os.path.dirname(sys.argv[0])
    else:
        full_path = os.getcwd() + "/" + os.path.dirname(sys.argv[0])
else:
    full_path = os.getcwd()
sys.path.insert(0, os.path.dirname(full_path))

def read_settings():
  with open(CONFIG_FILE_PATH) as f:
    settings = f.read()
  settings = eval(settings)
  default_settings.update(settings)
  globals().update(settings)
  print('successfully loaded the settings!')

def write_default_settings():
  config_folder = os.path.split(CONFIG_FILE_PATH)[0]
  if not os.path.exists(config_folder):
    try:
      os.makedirs(config_folder)
    except Exception:
      pass
  try:
    with open(CONFIG_FILE_PATH, 'w') as f:
      pprint(default_settings, f)
  except Exception:
    pass

# read the settings
try:
  # load the default settings
  globals().update(default_settings)
  # read the user settings
  read_settings()
except Exception:
  pass
finally:
  # write the default settings if it does not exist
  write_default_settings()

## indicator category
if INDICATOR_CATEGORY in ['SYSTEM_SERVICES','APPLICATION_STATUS','COMMUNICATIONS','HARDWARE','OTHER',]:
  exec('INDICATOR_CATEGORY = appindicator.CATEGORY_' + INDICATOR_CATEGORY)
else:
  exec('INDICATOR_CATEGORY = appindicator.CATEGORY_HARDWARE')

    

class PersianCalendar:
  def __init__(self):
    self.date = JalaliDate.today()
    self.base_folder = full_path
    self.icon_name = ICON_NAME
    self.icon_folder = DEFAULT_ICON_FOLDER
    self.ind = appindicator.Indicator("persian-calendar-indicator",
                       self.icon_name.format(day=self.date.day),
                       INDICATOR_CATEGORY,
                       os.path.join(self.base_folder, self.icon_folder)) 
    self.ind.set_status(appindicator.STATUS_ACTIVE)

    self.menu_setup()
    self.ind.set_menu(self.menu)
    # self.iterator = 0

  def menu_setup(self):
    self.menu = gtk.Menu()

    self.today_item = gtk.MenuItem('Today')
    self.today_item.show()
    
    self.quit_item = gtk.MenuItem("خروج")
    self.quit_item.connect("activate", self.quit)
    self.quit_item.show()

    self.toggle_icon_item = gtk.MenuItem("تغییر رنگ نقشک")
    self.toggle_icon_item.connect("activate", self.toggle_icon)
    self.toggle_icon_item.show()

    self.menu.append(self.today_item)
    self.menu.append(self.toggle_icon_item)
    self.menu.append(self.quit_item)

  def main(self):
    self.update_interface()
    gtk.timeout_add(PING_FREQUENCY * 1000, self.update_interface)

  def quit(self, widget):
    sys.exit(0)

  def get_date(self, frmt=DATE_FORMAT):
    return self.date.strftime(frmt)

  def update_interface(self):
    self.change_time()
    self.set_icon()
    # self.iterator += 1
    # if self.iterator > 30:
    #   self.iterator = 1
    # print('INFO:: updated the interface!')
    # we should return True to make sure this function get's called again and again
    return True

  def change_time(self):
    self.date = JalaliDate.today()
    # self.date.day += self.iterator
    self.today_item.set_label(self.get_date())

  def set_icon(self):
    if DEBUG:
      print('INFO:: icon folder:', os.path.join(self.base_folder, self.icon_folder))
    self.ind.set_icon_theme_path(os.path.join(self.base_folder, self.icon_folder))
    self.ind.set_icon(self.icon_name.format(day=self.date.day))

  def toggle_icon(self, *args):
    if self.icon_folder == ICON_FOLDER_DARK:
      self.icon_folder = ICON_FOLDER_LIGHT
      DEFAULT_ICON_FOLDER = ICON_FOLDER_LIGHT
    else:
      self.icon_folder = ICON_FOLDER_DARK
      DEFAULT_ICON_FOLDER = ICON_FOLDER_DARK
    self.set_icon()
    if DEBUG:
      print('INFO:: icon toggled!', self.icon_folder)
    try:
      default_settings['DEFAULT_ICON_FOLDER'] = DEFAULT_ICON_FOLDER
      write_default_settings()
    except Exception:
      pass


if __name__ == "__main__":
  indicator = PersianCalendar()
  indicator.main()
  gtk.main()
