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
from gettext import gettext as _
import logging
logger = logging.getLogger(__name__)

from gi.repository import Gtk, GLib, PeasGtk

from . import log

AUTOSTART_DESKTOPFILE_PATH = os.path.join(GLib.get_user_config_dir(),
                                          'autostart/gahshomar.desktop')


class Handler(object):
    """docstring for Handler"""

    @log
    def __init__(self, app):
        super().__init__()
        self.app = app

    @log
    def on_StartupSwitch_notify_active(self, startup_switch, data=None):
        if not startup_switch.get_active():
            try:
                os.remove(AUTOSTART_DESKTOPFILE_PATH)
            except Exception:
                pass
            startup_switch.set_active(False)
        else:
            try:
                with open(AUTOSTART_DESKTOPFILE_PATH, 'w') as f:
                    f.write('''[Desktop Entry]
Name=Gahshomar
Comment=View Georgian and Persian calendars
Icon=gahshomar
Exec=gahshomar -m
Terminal=false
Type=Application
Categories=GNOME;GTK;Productivty;Calendar;
StartupNotify=true
''')
            except Exception:
                logger.warning('', exc_info=True)
            startup_switch.set_active(True)
        return True


class SettingsWindow(Gtk.Dialog):
    """docstring for SettingsWindow"""
    @log
    def __init__(self, app):
        super().__init__(title=_('Gahshomar Preferences'), use_header_bar=True)
        self.app = app
        self.set_position(Gtk.WindowPosition.CENTER_ON_PARENT)
        self.resize(600, 480)

        builder = Gtk.Builder()
        builder.add_from_resource('/org/gahshomar/Gahshomar/prefs.ui')
        self.nb = builder.get_object('PreferencesNotebook')
        self.get_children()[0].pack_start(self.nb, True, True, 0)
        self.nb.show()
        builder.get_object('GeneralTabAlign').show()
        builder.get_object('GeneralTabBox').show()
        builder.get_object('StartupBox').show_all()
        self.startup_switch = builder.get_object('StartupSwitch')

        # add the plugin manager
        builder.get_object('PluginTabAlign').show()
        builder.get_object('PluginTabBox').show()
        self.PluginTabBox = builder.get_object('PluginTabBox')
        manager = PeasGtk.PluginManager()
        manager.show_all()
        self.PluginTabBox.pack_start(manager, True, True, 0)
        # read the settings and update
        self.refresh()

        # connect the signals
        builder.connect_signals(Handler(self.app))

    @log
    def refresh(self):
        if os.path.isfile(AUTOSTART_DESKTOPFILE_PATH):
            self.startup_switch.set_active(True)
        else:
            self.startup_switch.set_active(False)
