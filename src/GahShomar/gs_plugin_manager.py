#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Adopted from http://www.micahcarrick.com/python-gtk-plugins-with-yapsy.html
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

import os
import logging
logger = logging.getLogger(__name__)
from yapsy.ConfigurablePluginManager import ConfigurablePluginManager
from yapsy.VersionedPluginManager import VersionedPluginManager
from yapsy.PluginManager import PluginManagerSingleton
from gi.repository import Gtk, GObject


class GSPluginManager:
    """
    GahShomar Plugin Manager
    """
    def __init__(self, win):
        self.app = win.app
        self.parent = win

        # Build a list of directories which may contain plugins. This will
        # include the 'plugins' folder where this file resides as well as every
        # directory in xdg.BaseDirectory.xdg_data_dirs. This way users can
        # install plugins in something like ~/.local/yapsy-gtk-example/plugins
        # but your installer could also install those plugins to something like
        # /usr/share/yapsy-gtk-example/plugins. You'll see Yapsy checking each
        # of these directories if logging is set to logging.DEBUG
        xdg_data_dirs = [os.path.join(os.path.expanduser("~"),
                         '.local', 'share')]
        this_dir = os.path.abspath(self.app.FULL_PATH)
        plugin_dir = os.path.join(this_dir, 'data', 'plugins')
        places = [plugin_dir, ]
        for path in xdg_data_dirs:
            places.append(os.path.join(path, self.app.APP_NAME, "plugins"))

        # The singleton versino of the Yapsy plugin manager is used rather than
        # passing around a PluginManager instance. Prior to getting the
        # singleton instance, some "plugin manager decorators" are installed to:
        # 1. Automatically save active and non-active plugins to the config file
        # 2. Ensure only the newest versions of plugins are used.
        # This call to setBehaviour() must occur before getting the singleton
        # instance.

        PluginManagerSingleton.setBehaviour([
            ConfigurablePluginManager,
            VersionedPluginManager,
        ])

        # Get singleton instance
        manager = PluginManagerSingleton.get()

        # I like to give the manager a reference to the application class so
        # that plugins can connect to signals and access windows through
        # the manager singleton.
        manager.app = self.app
        manager.parent = self.parent

        # Give manager the config file and a callback function to call when it
        # changes the config (eg. when a plugin is activated or deactivated).
        manager.setConfigParser(self.app.config, self.app.config.write_settings)

        # Setup a file extension for plugin information files. In this it's
        # just ".plugin" but you may want to do something specific to your
        # application like ".myapp-plugin"
        manager.setPluginInfoExtension("gs-plugin")

        # Pass the manager the list of plugin directories
        manager.setPluginPlaces(places)

        # CollectPlugins is a shortcut for locatePlugins() and loadPlugins().
        manager.collectPlugins()

        # Now that the plugins have been collected, the plugin widget can
        # be refreshed to display all installed plugins.

        # self._create_window()
        # self._plugin_list = self.app.gs_settings_win._plugin_list
        # self._plugin_list.refresh()


class PluginList(Gtk.Box):
    __gtype_name__ = "PluginManager"
    """
    A composite widget which contains a tree view of installed plugins allowing
    a user to activate and de-activate the plugins and a toolbar to view the
    plugin information and refresh the list.
    """
    def __init__(self, parent=None):
        super().__init__(orientation=Gtk.Orientation.VERTICAL)
        self.parent = parent

        # # toolbar
        # toolbar = Gtk.Toolbar()
        # toolbar.set_icon_size(Gtk.IconSize.MENU)

        # button = Gtk.ToolButton.new_from_stock(Gtk.STOCK_REFRESH)
        # button.connect("clicked", self._on_refresh_clicked)
        # toolbar.insert(button, -1)

        # toolbar.insert(Gtk.SeparatorToolItem.new(), -1)

        # button = Gtk.ToolButton.new_from_stock(Gtk.STOCK_ABOUT)
        # button.set_sensitive(True)
        # button.connect("clicked", self._on_about_clicked)
        # toolbar.insert(button, -1)

        # self.pack_start(toolbar, False, True, 0)

        # plugin list
        self._treeview = PluginTreeView()
        sw = Gtk.ScrolledWindow()
        sw.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        sw.add(self._treeview)

        self.pack_start(sw, True, True, 0)
        self.show_all()

    # def _on_about_clicked(self, toolbutton, data=None):
    #     """ Show an 'About' dialog. """
    #     selection = self._treeview.get_selection()
    #     model, iter = selection.get_selected()
    #     if iter:
    #         info = model[iter][4]
    #         dialog = Gtk.AboutDialog()
    #         dialog.set_transient_for(self.parent)
    #         dialog.set_modal(True)
    #         dialog.set_authors((info.author,))
    #         dialog.set_website(info.website)
    #         dialog.set_website_label(info.website)
    #         dialog.set_program_name(info.name)
    #         dialog.set_version(str(info.version))
    #         dialog.set_comments(info.description)
    #         dialog.run()
    #         dialog.destroy()

    # def _on_refresh_clicked(self, toolbutton, data=None):
    #     self._treeview.refresh()

    def refresh(self):
        self._treeview.refresh()
        self.show_all()


class PluginTreeView(Gtk.TreeView):
    __gtype_name__ = "PluginTreeView"
    """
    A Gtk.TreeView widget populated with installed plugins allowing a user to
    activate and deactivate the plugins.
    """
    plugin_icon = None

    def __init__(self):

        self._store = Gtk.ListStore(GObject.TYPE_BOOLEAN,   # activated
                                    # GdkPixbuf.Pixbuf,       # icon
                                    GObject.TYPE_STRING,    # name
                                    GObject.TYPE_STRING,    # version
                                    object)                 # plugin info
        super().__init__(self._store)
        self.set_headers_visible(True)
        self.get_selection().set_mode(Gtk.SelectionMode.BROWSE)

        column = Gtk.TreeViewColumn("Plugin")
        cell = Gtk.CellRendererToggle()
        cell.connect("toggled", self._on_active_toggled)
        column.pack_start(cell, True)
        column.add_attribute(cell, 'active', 0)
        # cell = Gtk.CellRendererPixbuf()
        # column.pack_start(cell, False)
        # column.add_attribute(cell, 'pixbuf', 1)
        cell = Gtk.CellRendererText()
        column.pack_start(cell, True)
        column.add_attribute(cell, 'text', 1)
        self.append_column(column)

        column = Gtk.TreeViewColumn("Version")
        cell = Gtk.CellRendererText()
        column.pack_start(cell, True)
        column.add_attribute(cell, 'text', 2)
        self.append_column(column)

        # this_dir = os.path.abspath(os.path.dirname(__file__))
        # icon_file = os.path.join(this_dir, "plugin.png")
        # self.plugin_icon = GdkPixbuf.Pixbuf.new_from_file(icon_file)

    def _on_active_toggled(self, cell, path, data=None):
        # toggle the check box
        iter1 = self._store.get_iter(path)
        self._store[iter1][0] = not self._store[iter1][0]

        # activate or deactivate the plugin
        manager = PluginManagerSingleton.get()
        if self._store[iter1][0]:
            manager.activatePluginByName(self._store[iter1][3].name)
        else:
            manager.deactivatePluginByName(self._store[iter1][3].name)

    def refresh(self):
        self._store.clear()
        manager = PluginManagerSingleton.get()
        logger.debug('{} plugin(s) loaded'.format(len(manager.getAllPlugins())))
        for info in manager.getAllPlugins():
            plugin = info.plugin_object
            # print(plugin, (plugin.is_activated, info.name,
            #                str(info.version), info))
            # , self.plugin_icon
            self._store.append((plugin.is_activated, info.name,
                                str(info.version), info))
        if len(self._store):
            self.get_selection().select_iter(self._store.get_iter_first())
