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
import logging
logger = logging.getLogger(__name__)
from gi.repository import Gtk

from .gs_plugin_manager import PluginList


class Handler:
    """docstring for Handler"""
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app

    def on_spinbutton_ping_freq_value_changed(self, spin_button, data=None):
        value = spin_button.get_value_as_int()
        logger.debug('read {} from spinbutton_ping_freq.'.format(value))
        if 1 <= value <= 3600:
            self.app.config.set('Global', 'ping_frequency', str(value))
        else:
            value = int(self.app.config['Global']['ping_frequency'])
            spin_button.set_value(value)

    def on_switch_verbose_state_set(self, switch, active, data=None):
        self.app.config.set('Global', 'verbose', str(active))
        logger.debug('Changed verbose settings to {}'.format(active))
        switch.set_state(switch.get_active())
        return True

    def on_entry_date_format_activate(self, entry, data=None):
        text = entry.get_text()
        self.app.config.set('AppIndicator', 'date_format', text)
        logger.debug(
            'Changed config[AppIndicator][date_format] to {}'.format(text))

    def on_combobox_icon_name_changed(self, widget, data=None):
        tree_iter = widget.get_active()
        if tree_iter == 0:
            dark = 'dark'
        elif tree_iter == 1:
            dark = 'light'
        else:
            dark = 'alpha'
        text = 'gahshomar-{}-theme-'.format(dark) + '{day}'
        self.app.config['AppIndicator']['icon_name'] = text
        logger.debug(
            "Changed config['AppIndicator']['icon_name'] to {}".format(text))
        self.app.win.ind.set_icon()

    def on_combobox_indicator_category_changed(self, widget, data=None):
        tree_iter = widget.get_active()
        cat = self.parent.cats[tree_iter]
        self.app.config['AppIndicator']['indicator_category'] = cat
        log = "Changed config['AppIndicator']['indicator_category'] to {}"
        log = log.format(cat)
        logger.debug(log)

    def on_button_revert_clicked(self, button, data=None):
        self.app.config.read_default_settings()
        self.parent.refresh()
        logger.debug('Settings restored.')


class SettingsWindow(object):
    """docstring for SettingsWindow"""
    def __init__(self, app):
        super().__init__()
        self.app = app
        path = os.path.join(os.path.dirname(__file__), "gs_settings_page.glade")
        builder = Gtk.Builder()
        builder.add_from_file(path)
        self.builder = builder
        self.dialog = builder.get_object('gs_settings_dialog')
        self.spin = self.builder.get_object('spinbutton_ping_freq')
        self.switch_verbose = builder.get_object('switch_verbose')
        self.entry_date_format = builder.get_object('entry_date_format')
        self.combobox_icon_name = builder.get_object('combobox_icon_name')
        self.combobox_indicator_category = builder.get_object(
            'combobox_indicator_category')
        self.cats = ['SYSTEM_SERVICES', 'APPLICATION_STATUS', 'COMMUNICATIONS',
                     'HARDWARE', 'OTHER']
        self.notebook_settings = builder.get_object('notebook_settings')

        # tweak the interface
        self._spinbutton_ping_freq()
        self._create_plugin_page()

        # read the settings and update
        self.refresh()

        # connect the signals
        builder.connect_signals(Handler(self, self.app))

    def _spinbutton_ping_freq(self):
        self.spin.set_range(1, 3600)
        self.spin.set_increments(1, 1)

    def _create_plugin_page(self):
        """
        Create the main application window and store a reference to it in a
        public property so that plugins can access it.
        """
        nb = self.notebook_settings
        self._plugin_list = PluginList(nb)
        self._plugin_list.refresh()
        nb.append_page(self._plugin_list, Gtk.Label('Plugins'))
        # '# debug'
        # nb.set_current_page(2)
        # '# debug'
        nb.show_all()

    def refresh(self):
        self.spin.set_value(int(self.app.config['Global']['ping_frequency']))

        state = self.app.config['Global']['verbose'] == 'True'
        self.switch_verbose.set_active(state)
        self.switch_verbose.set_state(state)

        text = self.app.config['AppIndicator']['date_format']
        self.entry_date_format.set_text(text)

        dark = self.app.config['AppIndicator']['icon_name']
        if 'dark' in dark:
            tree_iter = 0
        elif 'light' in dark:
            tree_iter = 1
        elif 'alpha' in dark:
            tree_iter = 2
        else:
            tree_iter = 2
        self.combobox_icon_name.set_active(tree_iter)

        cat = self.app.config['AppIndicator']['indicator_category']
        tree_iter = self.cats.index(cat)
        self.combobox_indicator_category.set_active(tree_iter)

    def get_dialog(self):
        self.__init__(self.app)
        # self._plugin_list.refresh()
        return self.dialog
