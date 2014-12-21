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
import logging
logger = logging.getLogger(__name__)
from gi.repository import Gtk, GLib, Gio

from .gs_calendar_widget import PersianCalendarWidget, GeorgianCalendarWidget
from .gs_day_widget import PersianDayWidget, GeorgianDayWidget
from .gs_events_handler import EventsHandler
from .gs_indicator import GahShomarIndicator, USE_IND
from . import gs_settings_page
from .gs_plugin_manager import GSPluginManager

MENU_XML = """
<interface>
  <menu id='app-menu'>
    <section>
      <item>
        <attribute name='label' translatable='yes'>_About</attribute>
        <attribute name='action'>app.about</attribute>
      </item>
      <item>
        <attribute name='label' translatable='yes'>_Preferences</attribute>
        <attribute name='action'>app.preferences</attribute>
      </item>
    </section>
    <section>
      <item>
        <attribute name='label' translatable='yes'>_Quit</attribute>
        <attribute name='action'>app.quit</attribute>
        <attribute name='accel'>&lt;Primary&gt;q</attribute>
      </item>
    </section>
  </menu>
</interface>
"""

ABOUT_PAGE = '''
<interface>
  <object class="GtkAboutDialog" id="aboutdialog1">
    <property name="can_focus">False</property>
    <property name="title" translatable="yes">درباره برنامه</property>
    <property name="type_hint">dialog</property>
    <property name="program_name">گاه‌شمار</property>
    <property name="version">3.0.4</property>
    <property name="copyright" translatable="yes">Amir Mohammadi &lt;183.amir@gmail.com&gt;</property>
    <property name="comments" translatable="yes">گاه‌شمار (تقویم) ایرانی</property>
    <property name="website">http://183amir.github.io/gahshomar/</property>
    <property name="authors">Amir Mohammadi</property>
    <property name="logo">{FULL_PATH}/data/icons/gahshomar-logo.png</property>
    <property name="license_type">gpl-2-0</property>
    <child internal-child="vbox">
      <object class="GtkBox" id="aboutdialog-vbox1">
        <property name="can_focus">False</property>
        <property name="orientation">vertical</property>
        <property name="spacing">2</property>
        <child internal-child="action_area">
          <object class="GtkButtonBox" id="aboutdialog-action_area1">
            <property name="can_focus">False</property>
            <property name="layout_style">end</property>
            <child>
              <placeholder/>
            </child>
            <child>
              <placeholder/>
            </child>
          </object>
          <packing>
            <property name="expand">False</property>
            <property name="fill">False</property>
            <property name="position">0</property>
          </packing>
        </child>
        <child>
          <placeholder/>
        </child>
      </object>
    </child>
  </object>
</interface>
'''


class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, application, FULL_PATH, config, date=None):
        super().__init__(title='گاه‌شمار', application=application)

        if date is None:
            date = datetime.date.today()
        self.date = date

        # config values
        self.full_path = FULL_PATH
        self.config = config
        self.app = application

        pday = PersianDayWidget()
        gday = GeorgianDayWidget()
        self.day_widgets = [pday, gday]

        pcal = PersianCalendarWidget(date)
        pcal.parent = self
        gcal = GeorgianCalendarWidget(date)
        gcal.parent = self
        self.calendars = [pcal, gcal]
        self.handler = EventsHandler(self)

        self.main_grid = Gtk.Grid()
        main_grid = self.main_grid
        self.add(main_grid)
        main_grid.set_column_homogeneous(True)
        main_grid.set_column_spacing(spacing=20)
        # main_grid.set_row_homogeneous(True)
        main_grid.set_row_spacing(spacing=20)

        # setup appindicator
        self.visible = True
        self.setup_appindicator()

        # check if unity is running
        import os
        xdg_current_desktop = os.environ.get('XDG_CURRENT_DESKTOP').lower()
        self.xdg_current_desktop = xdg_current_desktop
        self.draw_interface()

        # update interface every 5 seconds
        GLib.timeout_add_seconds(int(self.config['Global']['ping_frequency']),
                                 self.handler.update_everything)

        # set the icon for the window
        self.connect('style-set', self.set_icon_)

        try:
            self.plugin_manager = GSPluginManager(self)
        except Exception:
            logger.exception(Exception)
        self.gs_settings_win = gs_settings_page.SettingsWindow(self.app)

    def draw_interface(self):

        xdg_current_desktop = self.xdg_current_desktop
        if 'unity' in xdg_current_desktop:
            self.offset = 1
        else:
            self.offset = 0
        # logger.debug('main_grid self.offset is {}'.format(self.offset))
        main_grid = self.main_grid
        for _ in range(len(self.calendars)+1):
            main_grid.remove_column(0)
        for i, v in enumerate(self.day_widgets):
            main_grid.attach(v, i, 0+self.offset, 1, 1)
        for i, v in enumerate(self.calendars):
            main_grid.attach(v, i, 1+self.offset, 1, 1)
        # main_grid.attach(Gtk.VSeparator(), 1, 0, 1, 2)
        self.setup_header_bar()

    def setup_header_bar(self):
        xdg_current_desktop = self.xdg_current_desktop
        today_button = Gtk.Button(label='امروز')
        today_button.connect("clicked", self.set_today)
        close_button = Gtk.Button.new_from_icon_name(
            'window-close-symbolic', Gtk.IconSize.BUTTON)
        close_button.connect('clicked', self.toggle_main_win)

        if 'unity' in xdg_current_desktop:
            toolbar = Gtk.Toolbar()
            sep = Gtk.SeparatorToolItem()
            sep.set_expand(True)
            sep.set_draw(False)
            toolbar.add(sep)
            tb_today = Gtk.ToolButton.new(today_button)
            tb_today.connect("clicked", self.set_today)
            toolbar.add(tb_today)
            self.connect("delete-event", self.toggle_main_win)
            # tb_close = Gtk.ToolButton.new(close_button)
            # tb_close.connect('clicked', self.toggle_main_win)
            # toolbar.add(tb_close)
            self.main_grid.attach(toolbar, 0, 0, 2, 1)
        else:
            # set header bar
            self.hb = Gtk.HeaderBar()
            self.hb.props.title = 'گاه‌شمار'

            if USE_IND:
                self.hb.props.show_close_button = False
                self.hb.pack_end(close_button)
            else:
                self.hb.props.show_close_button = True

            self.hb.pack_end(today_button)

            self.set_titlebar(self.hb)

    def on_settings_clicked(self):
        dialog = self.gs_settings_win.get_dialog()
        self.dialog = dialog
        # dialog.__init__()
        dialog.set_transient_for(self)
        # dialog.set_decorated(True)
        dialog.run()
        dialog.destroy()
        self.config.write_settings()
        logger.debug('Wrote the settings')

    def set_today(self, *args):
        self.handler.update_everything(datetime.date.today())

    def toggle_main_win(self, *args):
        if not USE_IND:
            return

        if self.visible:
            self.hide()
            self.visible = False
        else:
            self.show_all()
            self.present()
            self.visible = True
        return True

    def setup_appindicator(self):
        self.ind = GahShomarIndicator(self, self.date)

    def set_icon_(self, *args):
        # day = khayyam.JalaliDate.today().day
        icon = Gtk.IconTheme.load_icon(
            Gtk.IconTheme(),
            'gahshomar',
            512, 0)
        self.set_icon(icon)


class GahShomar(Gtk.Application):
    def __init__(self, FULL_PATH, config, minimized=False):
        Gtk.Application.__init__(
            self, application_id="com.mohammadi.calendar.gahshomar",
            inactivity_timeout=3000, register_session=True)
        self.FULL_PATH = FULL_PATH
        self.config = config
        self.minimized = minimized
        self.connect("startup", self.startup)
        self.connect("activate", self.activate)

    def about_activated(self, action, data=None, dialog=None):
        dialog.set_transient_for(self.win)
        dialog.run()
        dialog.destroy()

    def preferences_activated(self, action, data=None):
        self.win.on_settings_clicked()
        # import sys
        # import subprocess
        # if sys.platform.startswith('win32'):
        #     xdgopen = 'start'
        # if sys.platform.startswith('darwin'):
        #     xdgopen = 'open'
        # else:
        #     xdgopen = 'xdg-open'
        # args = [xdgopen, '{}'.format(path)]
        # subprocess.Popen(args)

    def new_window(self):
        self.win = MainWindow(self, self.FULL_PATH, self.config)

    def show_window(self):
        if not self.minimized:
            self.win.show_all()
        else:
            self.win.visible = False

    def activate(self, data=None):
        self.show_window()

    def startup(self, data=None):
        builder = Gtk.Builder()
        builder.add_from_string(ABOUT_PAGE.format(FULL_PATH=self.FULL_PATH))
        dialog = builder.get_object('aboutdialog1')

        action = Gio.SimpleAction(name="about")
        action.connect("activate", self.about_activated, dialog)
        self.add_action(action)

        action = Gio.SimpleAction(name="preferences")
        action.connect("activate", self.preferences_activated)
        self.add_action(action)

        action = Gio.SimpleAction(name="quit")
        action.connect("activate", lambda a, b: self.quit())
        self.add_action(action)

        builder = Gtk.Builder()
        builder.add_from_string(MENU_XML)
        self.set_app_menu(builder.get_object("app-menu"))

        self.new_window()
