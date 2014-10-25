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

from gi.repository import Gtk


class SettingsWindow(Gtk.Window):
    """SettingsWindow"""
    def __init__(self, parent):
        super().__init__(title='شخصی‌سازی')
        self.parent = parent

        # notebook window
        ntbk = Gtk.Notebook()
        # ntbk.set_tab_pos()  # Gtk.PositionType.LEFT
        self.ntbk = ntbk
        self.add(ntbk)

        self.setup_pages()

    def setup_pages(self):
        config = self.parent.config

        # Global settings
        listbox = Gtk.ListBox()
        self.ntbk.append_page(listbox, Gtk.Label('Global'))
        box = Gtk.Box(spacing=20)
        listbox.add(box)
        label = Gtk.Label('Update Frequency')
        buffer1 = Gtk.EntryBuffer()
        buffer1.set_text(config['Global']['ping_frequency'], -1)
        text_entry = Gtk.Entry.new_with_buffer(buffer1)
        box.pack_start(label, False, False, 0)
        box.pack_end(text_entry, False, False, 0)

        # AppIndicator settings
        listbox = Gtk.ListBox()
        self.ntbk.append_page(listbox, Gtk.Label('AppIndicator'))
        box = Gtk.Box(spacing=20)
        listbox.add(box)
        label = Gtk.Label('Date Format')
        buffer1 = Gtk.EntryBuffer()
        buffer1.set_text(config['AppIndicator']['date_format'], -1)
        text_entry = Gtk.Entry.new_with_buffer(buffer1)
        box.pack_start(label, False, False, 0)
        box.pack_end(text_entry, False, False, 0)

        box = Gtk.Box(spacing=20)
        listbox.add(box)
        label = Gtk.Label('Default Icon Folder')
        buffer1 = Gtk.EntryBuffer()
        buffer1.set_text(config['AppIndicator']['default_icon_folder'], -1)
        text_entry = Gtk.Entry.new_with_buffer(buffer1)
        text_entry.set_size_request(
            15*len(config['AppIndicator']['default_icon_folder']), -1)
        box.pack_start(label, False, False, 0)
        box.pack_end(text_entry, False, False, 0)



'''
# GahShomar Config File
[Global]

# In seconds; the frequency of updating the date
ping_frequency = 5

# Prints more info in the terminal
verbose = False

# Applicatio Version (Do not edit this!)
version = 3.0

[AppIndicator]

# Day of the week, day month year
date_format = %A، %d %B %Y

# name of the icon file
icon_name = persian-calendar-{day}

# the folder to look for icons
default_icon_folder = data/icons/ubuntu-mono-dark

icon_folder_dark = data/icons/ubuntu-mono-dark

# if you are using a light theme, you can use this icon
icon_folder_light = data/icons/ubuntu-mono-light


# possible values are SYSTEM_SERVICES APPLICATION_STATUS
# COMMUNICATIONS HARDWARE  OTHER
indicator_category = APPLICATION_STATUS
'''