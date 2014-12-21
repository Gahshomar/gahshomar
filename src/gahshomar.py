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

import os
import sys
import argparse
import logging
logger = logging.getLogger(__file__)

APP_NAME = 'gahshomar'

# argument parser
parser = argparse.ArgumentParser()
parser.add_argument('-m', "--no-main-window",
                    help='does not display the main window',
                    action="store_true")
parser.add_argument('-v', "--verbose",
                    help='prints more info',
                    action="store_true")
args = parser.parse_args()

# change the logging information.
if args.verbose:
    logging.basicConfig(level=logging.DEBUG)
    logger.debug('Debugging options enabled.')

# get the full path of the file
if os.path.dirname(sys.argv[0]) != '.':
    if sys.argv[0][0] == os.sep:
        FULL_PATH = os.path.dirname(sys.argv[0])
    else:
        FULL_PATH = os.getcwd() + os.sep + os.path.dirname(sys.argv[0])
else:
    FULL_PATH = os.getcwd()

# add FULL_PATH to the system path
sys.path.insert(0, os.path.dirname(FULL_PATH))

from GahShomar.gs_settings import GSConfigParser
# load the settings
CONFIG_FILE_PATH = os.path.join(
    os.path.expanduser("~"), '.config', APP_NAME, 'settings.conf')
config = GSConfigParser(CONFIG_FILE_PATH, interpolation=None)

# read the settings
try:
    # load the default settings
    config.read_default_settings()
    current_version = float(config['Global']['version'])
    # read the user settings
    config.read_settings()
    old_version = float(config['Global']['version'])
    if current_version == 3.2 and current_version > old_version:
        config.read_default_settings()
        try:
            os.remove(CONFIG_FILE_PATH)
        except Exception:
            pass
except Exception:
    logger.exception(Exception)
finally:
    # write the settings
    config.write_settings()

# change the logging information.
if args.verbose or config['Global']['verbose'] == 'True':
    logging.basicConfig(level=logging.DEBUG)

if __name__ == '__main__':
    from GahShomar.gs_main_window import GahShomar
    app = GahShomar(FULL_PATH, config, args.no_main_window)
    app.APP_NAME = APP_NAME
    r = app.run()
