# main.py
#
# Copyright (C) 2017 Amir MOHAMMADI
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import logging
import sys
import gi

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, Gio

from .window import GahshomarWindow
from .preferences import GahshomarPreferences
from .api import GahshomarApi


class Application(Gtk.Application):
    def __init__(self):
        super().__init__(application_id='org.gahshomar.Gahshomar',
                         flags=Gio.ApplicationFlags.FLAGS_NONE)

    def do_activate(self):
        win = self.props.active_window
        if not win:
            win = GahshomarWindow(application=self)
        win.present()

    def do_startup(self):
        Gtk.Application.do_startup(self)

        action = Gio.SimpleAction.new("about", None)
        action.connect("activate", self.on_about)
        self.add_action(action)

        action = Gio.SimpleAction.new("quit", None)
        action.connect("activate", self.on_quit)
        self.add_action(action)

        action = Gio.SimpleAction.new("preferences", None)
        action.connect("activate", self.on_preferences)
        self.add_action(action)

        builder = Gtk.Builder.new_from_resource(
            '/org/gahshomar/Gahshomar/app-menu.ui')
        self.set_app_menu(builder.get_object("app-menu"))

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
    logging.basicConfig(level=logging.DEBUG)
    # logger = logging.getLogger(__name__)
    # logger.setLevel(logging.DEBUG)
    # root_logger.addHandler(logging.StreamHandler())
    # root_logger.setLevel(logging.DEBUG)
    app = Application()
    return app.run(sys.argv)
