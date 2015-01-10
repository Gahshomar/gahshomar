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

import datetime
from gettext import gettext as _
import logging
logger = logging.getLogger(__name__)

from gi.repository import Gtk, GObject, Gio, GLib
import gahshomar.khayyam as khayyam


class Indicator(GObject.GObject):
    def __init__(self, app=None):
        super().__init__()
        try:
            from gi.repository import AppIndicator3 as appindicator
        except ImportError:
            logger.exception(ImportError)
            return

        self.date = datetime.date.today()
        self.app = app

        self.settings = Gio.Settings.new('org.gahshomar.Gahshomar')
        self.date_format = str(self.settings.get_value('persian-date-format'))
        self.date_format = self.date_format.replace("'", "")

        self.ind = appindicator.Indicator.new(
            "GahShomar-indicator",
            'gahshomar',
            appindicator.IndicatorCategory.APPLICATION_STATUS)
        self.ind.set_status(appindicator.IndicatorStatus.ACTIVE)

        self.menu_setup()
        self.update()

        GLib.timeout_add_seconds(5, self.update)

    def menu_setup(self):
        self.menu = Gtk.Menu()
        self.menu.set_halign(Gtk.Align.CENTER)

        self.today_item = Gtk.MenuItem(_('Today'))
        self.today_item.connect("activate", self.activate)
        self.today_item.show()

        self.quit_item = Gtk.MenuItem(_('Quit'))
        self.quit_item.connect("activate", self.quit)
        self.quit_item.show()

        self.menu.append(self.today_item)
        self.menu.append(self.quit_item)
        self.ind.set_menu(self.menu)

    def get_date_formatted(self, frmt=None):
        if frmt is None:
            frmt = self.date_format
        text = khayyam.JalaliDate.from_date(self.date).strftime(frmt)
        if text[0] == '0' or text[0] == '۰':
            text = text[1:]
        return text

    def quit(self, widget):
        self.app.quit()

    def update(self):
        self.date = datetime.date.today()
        self.today_item.set_label(_(self.get_date_formatted()))
        self.ind.set_label(_(self.get_date_formatted('%d')), _('Gahshomar'))

        # make sure to return True so that it keeps updating
        return True

    def activate(self, *args):
        self.app.do_activate()
