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

from gi.repository import Gtk, GLib, Gio, PeasGtk

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

    @log
    def on_HeaderBarSwitch_active_notify(self, switch, data=None):
        self.settings = Gio.Settings.new('org.gahshomar.Gahshomar')
        if switch.get_active():
            self.settings.set_value('header-bar',
                                    GLib.Variant.new_boolean(True))
        else:
            self.settings.set_value('header-bar',
                                    GLib.Variant.new_boolean(False))
        warnmsg = Gtk.MessageDialog(
            text=_('You need to restart the application for changes'
                   ' to take effect'),
            message_type=Gtk.MessageType.WARNING,
            buttons=Gtk.ButtonsType.CLOSE,
            transient_for=self.app.setting_win)
        warnmsg.run()
        warnmsg.destroy()


class SettingsWindow(Gtk.Dialog):
    """docstring for SettingsWindow"""
    @log
    def __init__(self, app):
        super().__init__(title=_('Gahshomar Preferences'))
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
        builder.get_object('HeaderBarBox').show_all()
        self.startup_switch = builder.get_object('StartupSwitch')
        self.header_bar_switch = builder.get_object('HeaderBarSwitch')

        # add the plugin manager
        builder.get_object('PluginTabAlign').show()
        builder.get_object('PluginTabBox').show()
        self.PluginTabBox = builder.get_object('PluginTabBox')
        manager = PeasGtk.PluginManager()
        manager.show_all()
        self.PluginTabBox.pack_start(manager, True, True, 0)
        # read the settings and update
        self.settings = Gio.Settings.new('org.gahshomar.Gahshomar')
        self.refresh()

        # connect the signals
        builder.connect_signals(Handler(self.app))

    @log
    def refresh(self):
        if os.path.isfile(AUTOSTART_DESKTOPFILE_PATH):
            self.startup_switch.set_active(True)
        else:
            self.startup_switch.set_active(False)

        if bool(self.settings.get_value('header-bar')):
            self.header_bar_switch.set_active(True)
        else:
            self.header_bar_switch.set_active(False)
