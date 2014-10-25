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

# do not modify this, modify ~/.config/persian-calendar/settings.conf
config_default_str = '''# GahShomar Config File
[Global]

# In seconds; the frequency of updating the date
ping_frequency = 5

# Prints more info in the terminal
verbose = False

# Applicatio Version (Do not edit this!)
version = 3.0

[AppIndicator]

# Day of the week, day month year
date_format = %A، %d %B %Y

# name of the icon file
icon_name = persian-calendar-{day}

# the folder to look for icons
default_icon_folder = data/icons/ubuntu-mono-dark

icon_folder_dark = data/icons/ubuntu-mono-dark

# if you are using a light theme, you can use this icon
icon_folder_light = data/icons/ubuntu-mono-light


# possible values are SYSTEM_SERVICES APPLICATION_STATUS
# COMMUNICATIONS HARDWARE  OTHER
indicator_category = APPLICATION_STATUS
'''

import os
import configparser
config = configparser.ConfigParser(interpolation=None)
CONFIG_FILE_PATH = os.path.join(
    os.path.expanduser("~"), '.config', 'persian-calendar', 'settings.conf')
CONFIG_FILE_PATH_OLD = os.path.join(
    os.path.expanduser("~"), '.config', 'persian-calendar', 'settings')


def read_settings():
    # config.update(config_default)
    config.read(CONFIG_FILE_PATH)
    # print('successfully loaded the settings!')


def write_default_settings():
    config_folder = os.path.split(CONFIG_FILE_PATH)[0]
    if not os.path.exists(config_folder):
        try:
            os.makedirs(config_folder)
        except Exception:
            pass
    try:
        if not os.path.exists(CONFIG_FILE_PATH):
            with open(CONFIG_FILE_PATH, 'w') as f:
                f.write(config_default_str)
    except Exception:
        pass


def write_settings():
    settings = config_default_str.split('\n')
    for section in config:
        for key, value in config[section].items():
            for i, line in enumerate(settings):
                line = line.strip()
                if len(line) > 0 and line[0] != '#' and line[0] != ';' and \
                        line[0] != '[':
                    key1, _ = line.split('=', 1)
                    key1 = key1.strip().lower()
                    if key1 == key:
                        if key == 'verbose':
                            value = 'False'
                        settings[i] = '{0} = {1}'.format(key, value)
    try:
        with open(CONFIG_FILE_PATH, 'w') as f:
            f.write('\n'.join(settings))
    except Exception:
        print(str(Exception))

config.write_settings = write_settings
# read the settings
try:
    # load the default settings
    config.read_string(config_default_str)
    # current_version = float(config['Global']['version'])
    # read the user settings
    read_settings()
    # old_version = float(config['Global']['version'])
except Exception:
    print(str(Exception))
finally:
    # write the default settings if it does not exist
    write_default_settings()

# remove old config file
try:
    os.remove(CONFIG_FILE_PATH_OLD)
except Exception:
    pass
