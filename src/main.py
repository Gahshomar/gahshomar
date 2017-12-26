# -*- Mode: Python; coding: utf-8; indent-tabs-mode: s; tab-width: 4 -*-

import logging
import sys
import gi

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')

from gi.repository import Gtk, Gio, AppIndicator3
from .window import GahshomarWindow
from .preferences import GahshomarPreferences
from .api import GahshomarApi
from .calendar import TODAY_PERSIAN
from .appindicator import AppIndicator


class Application(Gtk.Application):
    def __init__(self):
        super().__init__(
            application_id='org.gahshomar.Gahshomar',
            flags=Gio.ApplicationFlags.FLAGS_NONE)

    def do_activate(self):
        win = self.props.active_window
        if not win:
            win = GahshomarWindow(application=self)
        win.present()

    def do_startup(self):
        Gtk.Application.do_startup(self)

        # setup actions
        action = Gio.SimpleAction.new("about", None)
        action.connect("activate", self.on_about)
        self.add_action(action)

        action = Gio.SimpleAction.new("quit", None)
        action.connect("activate", self.on_quit)
        self.add_action(action)

        action = Gio.SimpleAction.new("preferences", None)
        action.connect("activate", self.on_preferences)
        self.add_action(action)

        # setup the app-menu
        builder = Gtk.Builder.new_from_resource(
            '/org/gahshomar/Gahshomar/app-menu.ui')
        self.set_app_menu(builder.get_object("app-menu"))

        # setup the appIndicator
        self.ind = AppIndicator(self, TODAY_PERSIAN)

        # increase ref count so the app does not go away. This enables the app
        # to run as a service. We do this because we provide a d-bus api.
        self.hold()

    def on_about(self, action, param):
        builder = Gtk.Builder.new_from_resource(
            '/org/gahshomar/Gahshomar/about-dialog.ui')
        about_dialog = builder.get_object("about-dialog")
        about_dialog.set_transient_for(self.props.active_window)
        about_dialog.present()

    def on_quit(self, action, param):
        self.quit()

    def on_preferences(self, action, param):
        win = GahshomarPreferences(transient_for=self.props.active_window)
        win.present()

    def do_dbus_register(self, connection, object_path):
        self.dbus_api = GahshomarApi(connection, object_path)
        return True

    def do_dbus_unregister(self, connection, object_path):
        del self.dbus_api


def main(version):
    log_format = '%(name)s@%(asctime)s -- %(levelname)s: %(message)s'
    logging.basicConfig(format=log_format, level=logging.DEBUG)
    # logger = logging.getLogger(__name__)
    # logger.setLevel(logging.DEBUG)
    # root_logger.addHandler(logging.StreamHandler())
    # root_logger.setLevel(logging.DEBUG)
    app = Application()
    return app.run(sys.argv)
