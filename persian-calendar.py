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
import re
import gtk
import appindicator

import khayyam

default_settings = {# do not modify this, modify ~/.config/persian-calendar/settings
'PING_FREQUENCY' : 10, # In seconds; the frequency of updating the date
'DATE_FORMAT' : u'%A، %d %B %Y', # Day of the week, day month year
'ICON_NAME' : "persian-calendar-{day}", # name of the icon file
'ICON_FOLDER_DARK' : "data/icons/ubuntu-mono-dark", # name of the icon file
'ICON_FOLDER_LIGHT' : "data/icons/ubuntu-mono-light", # if you are using a light theme, you can use this icon

'INDICATOR_CATEGORY' : 'HARDWARE',
# SYSTEM_SERVICES
# APPLICATION_STATUS
# COMMUNICATIONS
# HARDWARE
# OTHER
}

CONFIG_FILE_PATH = os.path.join(os.path.expanduser("~"), '.config', 'persian-calendar', 'settings')

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
      f.write(repr(default_settings))
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
exec('INDICATOR_CATEGORY = appindicator.CATEGORY_' + INDICATOR_CATEGORY)


NUM_DICT = {'0':'۰',
            '1':'۱',
            '2':'۲',
            '3':'۳',
            '4':'۴',
            '5':'۵',
            '6':'۶',
            '7':'۷',
            '8':'۸',
            '9':'۹'}

def latinN2PersianN(num):
  numP = ''
  for v in num:
    if v in NUM_DICT:
      numP += NUM_DICT[v]
    else:
      numP += v
  return numP

def _replace_if_match(data, pattern, new):
    if re.search(pattern, data):
        if callable(new):
            new = new()
        if not isinstance(new, basestring):
            new = unicode(new)
        return data.replace(pattern, latinN2PersianN(new))
    return data

class JalaliDate(khayyam.JalaliDate):
  """JalaliDate class with Persian numbers"""
  def strftime(self, frmt):
    """
=========    =======
Directive    Meaning
=========    =======
%a           Locale’s abbreviated weekday name.     
%A           Locale’s full weekday name.     
%b           Locale’s abbreviated month name.     
%B           Locale’s full month name.     
%d           Day of the month as a decimal number [01,31].     
%j           Day of the year as a decimal number [001,366].     
%m           Month as a decimal number [01,12].     
%U           Week number of the year (Sunday as the first day of the week) as a decimal number [00,53]. All days in a new year preceding the first Sunday are considered to be in week 0.    (4)
%w           Weekday as a decimal number [0(Sunday),6].     
%W           Week number of the year (Monday as the first day of the week) as a decimal number [00,53]. All days in a new year preceding the first Monday are considered to be in week 0.    (4)
%x           Locale’s appropriate date representation.     
%y           Year without century as a decimal number [00,99].     
%Y           Year with century as a decimal number.     
%%           A literal '%' character.
=========    =======
    """
    result = _replace_if_match(frmt,   '%Y', self.year)
    result = _replace_if_match(result, '%y', lambda: str(self.year)[-2:])
    result = _replace_if_match(result, '%m', self.month)
    result = _replace_if_match(result, '%d', self.day)
    result = _replace_if_match(result, '%a', self.weekdayabbr)
    result = _replace_if_match(result, '%A', self.weekdayname)
    result = _replace_if_match(result, '%b', self.monthabbr)
    result = _replace_if_match(result, '%B', self.monthname)
    result = _replace_if_match(result, '%x', self.localformat)
    result = _replace_if_match(result, '%j', self.dayofyear)
    result = _replace_if_match(result, '%U', lambda: self.weekofyear(6))
    result = _replace_if_match(result, '%W', lambda: self.weekofyear(0))
    result = _replace_if_match(result, '%w', self.weekday)
    result = _replace_if_match(result, '%%', '%')
    return result
    

class PersianCalendar:
  def __init__(self):
    self.date = JalaliDate.today()
    self.base_folder = os.path.join(os.path.dirname(sys.argv[0]))
    self.icon_name = ICON_NAME
    self.icon_folder = ICON_FOLDER_DARK
    self.ind = appindicator.Indicator("persian-calendar-indicator",
                       self.icon_name.format(day=self.date.day),
                       INDICATOR_CATEGORY,
                       os.path.join(self.base_folder, self.icon_folder)) 
    self.ind.set_status(appindicator.STATUS_ACTIVE)

    self.menu_setup()
    self.ind.set_menu(self.menu)

  def menu_setup(self):
    self.menu = gtk.Menu()

    self.today_item = gtk.MenuItem('Today')
    self.today_item.show()
    
    self.quit_item = gtk.MenuItem("Quit")
    self.quit_item.connect("activate", self.quit)
    self.quit_item.show()

    self.toggle_icon_item = gtk.MenuItem("Toggle Icon Color")
    self.toggle_icon_item.connect("activate", self.toggle_icon)
    self.toggle_icon_item.show()

    self.menu.append(self.today_item)
    self.menu.append(self.toggle_icon_item)
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
    self.date = JalaliDate.today()
    self.today_item.set_label(self.get_date())
    self.set_icon()

  def set_icon(self):
    self.ind.set_icon_theme_path(os.path.join(self.base_folder, self.icon_folder))
    self.ind.set_icon(self.icon_name.format(day=self.date.day))

  def toggle_icon(self, widget):
    if self.icon_folder == ICON_FOLDER_DARK:
      self.icon_folder = ICON_FOLDER_LIGHT
    else:
      self.icon_folder = ICON_FOLDER_DARK
    self.set_icon()


if __name__ == "__main__":
  indicator = PersianCalendar()
  indicator.main()
