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


from os.path import dirname
import logging
logger = logging.getLogger(__name__)
from configparser import SafeConfigParser

from .gs_util import make_dir


# do not modify this
config_default_str = '''# GahShomar Config File
[Global]

# In seconds; the frequency of updating the date
ping_frequency = 5

# Prints more info in the terminal
verbose = False

# Applicatio Version (Do not edit this!)
version = 3.2

[AppIndicator]

# name of the icon file (change "dark" to "light" to change the color of icons)
icon_name = gahshomar-dark-theme-{day}

# Day of the week, day month year
date_format = %A، %d %B %Y

# possible values are SYSTEM_SERVICES APPLICATION_STATUS
# COMMUNICATIONS HARDWARE  OTHER
indicator_category = APPLICATION_STATUS
'''


class GSConfigParser(SafeConfigParser):
    """A GSConfigParser for reading and writing the settings"""
    def __init__(self, path, interpolation=None):
        super().__init__(interpolation=interpolation)
        self.path = path

    def read_default_settings(self, clear=True):
        if clear:
            self.clear()
        self.read_string(config_default_str)

    def read_settings(self):
        self.read(self.path)
        logger.debug(
            'Successfully loaded the settings from {}'.format(self.path))

    def write_settings(self):
        try:
            make_dir(dirname(self.path))
            with open(self.path, 'w') as f:
                self.write(f)
            logger.debug('Wrote the settings on file: {}'.format(self.path))
        except Exception:
            logger.exception(Exception)
