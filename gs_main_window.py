#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
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

import datetime
from gi.repository import Gtk, GLib, Gio

from calendar_widget import PersianCalendarWidget, GeorgianCalendarWidget
from day_widget import PersianDayWidget, GeorgianDayWidget
from events_handler import EventsHandler
from gs_indicator import GahShomarIndicator, USE_IND
from gs_settings_page import SettingsWindow


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
    <property name="website">http://183amir.github.io/persian-calendar/</property>
    <property name="authors">Amir Mohammadi</property>
    <property name="logo">{FULL_PATH}/data/icons/persian-calendar-logo.png</property>
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

        self.draw_interface()

        # update interface every 5 seconds
        GLib.timeout_add_seconds(5, self.handler.update_everything)

        self.connect('style-set', self.set_icon_)

    def draw_interface(self):
        main_grid = self.main_grid
        for i, v in enumerate(self.day_widgets):
            main_grid.attach(v, i, 0, 1, 1)
        for i, v in enumerate(self.calendars):
            main_grid.attach(v, i, 1, 1, 1)
        # main_grid.attach(Gtk.VSeparator(), 1, 0, 1, 2)
        self.setup_header_bar()

    def setup_header_bar(self):
        # set header bar
        hb = Gtk.HeaderBar()
        hb.props.title = 'گاه‌شمار'

        if USE_IND:
            hb.props.show_close_button = False
            close_button = Gtk.Button.new_from_icon_name(
                'window-close-symbolic', Gtk.IconSize.BUTTON)
            close_button.connect('clicked', self.toggle_main_win)
            hb.pack_end(close_button)
        else:
            hb.props.show_close_button = True

        button = Gtk.Button(label='امروز')
        button.connect("clicked", self.set_today)
        hb.pack_end(button)

        # sett_button = Gtk.Button.new_from_icon_name(
        #     'preferences-system', Gtk.IconSize.LARGE_TOOLBAR)
        # sett_button.connect('clicked', self.on_settings_clicked)
        # hb.pack_end(sett_button)
        self.set_titlebar(hb)

    def on_settings_clicked(self, button):
        sett_win = SettingsWindow(self)
        sett_win.show_all()

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

    def setup_appindicator(self):
        self.ind = GahShomarIndicator(self, self.date)

    def set_icon_(self, *args):
        # day = khayyam.JalaliDate.today().day
        icon = Gtk.IconTheme.load_icon(
            Gtk.IconTheme(),
            'persian-calendar',
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

    def preferences_activated(self, action, data=None, path=None):
        import sys
        import subprocess
        if sys.platform.startswith('win32'):
            xdgopen = 'start'
        if sys.platform.startswith('darwin'):
            xdgopen = 'open'
        else:
            xdgopen = 'xdg-open'
        args = [xdgopen, '{}'.format(path)]
        subprocess.Popen(args)

    def new_window(self):
        win = MainWindow(self, self.FULL_PATH, self.config)
        if not self.minimized:
            win.show_all()
        else:
            win.visible = False
        self.win = win

    def activate(self, data=None):
        self.new_window()

    def startup(self, data=None):
        builder = Gtk.Builder()
        builder.add_from_string(ABOUT_PAGE.format(FULL_PATH=self.FULL_PATH))
        dialog = builder.get_object('aboutdialog1')

        action = Gio.SimpleAction(name="about")
        action.connect("activate", self.about_activated, dialog)
        self.add_action(action)

        action = Gio.SimpleAction(name="preferences")
        action.connect("activate", self.preferences_activated,
                       self.config.CONFIG_FILE_PATH)
        self.add_action(action)

        action = Gio.SimpleAction(name="quit")
        action.connect("activate", lambda a, b: self.quit())
        self.add_action(action)

        builder = Gtk.Builder()
        builder.add_from_string(MENU_XML)
        self.set_app_menu(builder.get_object("app-menu"))
