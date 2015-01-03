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

from gi.repository import Gtk, Gio, GLib, Gdk  # , Notify
from gettext import gettext as _
import logging
logger = logging.getLogger(__name__)

from gahshomar.window import Window
from gahshomar.indicator import Indicator
from gahshomar import log
from gahshomar.settings_page import SettingsWindow


class EventsHandler(object):
    """docstring for EventsHandler"""
    def __init__(self):
        super().__init__()
        self.updateables = list()

    def update_everything(self, **kwargs):
        for instance in self.updateables:
            instance.update(**kwargs)


class Application(Gtk.Application):
    @log
    def __init__(self, minimized=False):
        Gtk.Application.__init__(self,
                                 application_id='org.gahshomar.Gahshomar',
                                 flags=Gio.ApplicationFlags.FLAGS_NONE)
        GLib.set_application_name(_("Gahshomar"))
        GLib.set_prgname('gahshomar')
        self.settings = Gio.Settings.new('org.gahshomar.Gahshomar')
        # cssProviderFile = Gio.File.new_for_uri(
        #     'resource:///org/gahshomar/Gahshomar/application.css')
        # cssProvider = Gtk.CssProvider()
        # cssProvider.load_from_file(cssProviderFile)
        # screen = Gdk.Screen.get_default()
        # styleContext = Gtk.StyleContext()
        # styleContext.add_provider_for_screen(
        #     screen, cssProvider, Gtk.STYLE_PROVIDER_PRIORITY_USER)

        self._window = None
        self.minimized = minimized
        self.handler = EventsHandler()
        # the appindicator
        self.appind = None

    @log
    def build_app_menu(self):
        builder = Gtk.Builder()

        builder.add_from_resource('/org/gahshomar/Gahshomar/app-menu.ui')

        menu = builder.get_object('app-menu')
        self.set_app_menu(menu)

        aboutAction = Gio.SimpleAction.new('about', None)
        aboutAction.connect('activate', self.about)
        self.add_action(aboutAction)

        helpAction = Gio.SimpleAction.new('help', None)
        helpAction.connect('activate', self.help)
        self.add_action(helpAction)

        preferencesAction = Gio.SimpleAction.new('preferences', None)
        preferencesAction.connect('activate', self.preferences)
        self.add_action(preferencesAction)

        quitAction = Gio.SimpleAction.new('quit', None)
        quitAction.connect('activate', self.quit)
        self.add_action(quitAction)

    # @log
    # def do_dbus_register(self, connection, object_path):
    #     Gtk.Application.do_dbus_register(self, connection, object_path)
    #     print(self.list_actions())
    #     connection.export_action_group('/Actions', self.list_actions())

    def setup_dbus(self):
        # if self.get_is_registered():
            # logger.debug('app is registered.')
        from gahshomar.dbus_service import IndicatorBus
        import dbus.mainloop.glib
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
        # dbus_connection = self.get_dbus_connection()
        # self.dbus_object = IndicatorBus(conn=dbus_connection,
        #                                 object_path='/IndicatorBus',
        #                                 app=self)
        import dbus
        self.session_bus = dbus.SessionBus()
        logger.debug('self.session_bus: '+str(self.session_bus))
        self.dbus_name = dbus.service.BusName("org.gahshomar.GahshomarService",
                                              self.session_bus)
        logger.debug('self.dbus_name: '+str(self.dbus_name))
        self.dbus_object = IndicatorBus(conn=self.session_bus,
                                        object_path='/IndicatorBus',
                                        bus_name=self.dbus_name, app=self)
        logger.debug('self.dbus_object: '+str(self.dbus_object))

        # else:
        #     logger.debug('app is not registered.')
    @log
    def help(self, action, param):
        Gtk.show_uri(None, "help:gahshomar", Gdk.CURRENT_TIME)

    @log
    def about(self, action, param):
        builder = Gtk.Builder()
        builder.add_from_resource('/org/gahshomar/Gahshomar/AboutDialog.ui')
        about = builder.get_object('about_dialog')
        about.set_transient_for(self._window)
        about.connect("response", self.about_response)
        about.show()

    @log
    def about_response(self, dialog, response):
        dialog.destroy()

    @log
    def quit(self, action=None, param=None):
        self._window.destroy()

    @log
    def preferences(self, action=None, param=None):
        setting_win = SettingsWindow(self)
        setting_win.set_transient_for(self._window)
        setting_win.show()

    @log
    def do_startup(self):
        Gtk.Application.do_startup(self)
        # Notify.init(_("Gahshomar"))
        self.build_app_menu()
        self.setup_dbus()

    @log
    def do_activate(self):
        if not self._window:
            self._window = Window(self, self.minimized)
            # self.service = MediaPlayer2Service(self)
            # if self.settings.get_value('notifications'):
            #     self._notifications = NotificationManager(self._window.player)
            if not self.minimized:
                self._window.present()
            else:
                # make sure you hide the window only in the startup
                self.minimized = False
        else:
            self._window.present()

        # the appindicator
        if not self.appind:
            self.appind = Indicator(self)
