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

import logging
logger = logging.getLogger(__name__)
from concurrent.futures import ThreadPoolExecutor
import urllib

# third-party library imports
from yapsy.IPlugin import IPlugin
from yapsy.PluginManager import PluginManagerSingleton
from gi.repository import Gtk

# local imports
from GahShomar.gs_day_widget import GeorgianDayWidget, PersianDayWidget
from GahShomar.gs_calendar import date_to_georgian
from GahShomar.gs_util import cache

try:
    from icalendar import Calendar
except ImportError:
    logger.error('icalendar python package needs to be installed')

Executor = ThreadPoolExecutor(max_workers=4)


@cache
def loadics(url):
    if url.startswith('/'):
        path = url
    else:
        (path, message) = urllib.request.urlretrieve(url)
    with open(path, 'rb') as f:
        cal = Calendar.from_ical(f.read())
    return cal


class PersianDayWidgetWithWiki(PersianDayWidget):
    """docstring for PersianDayWidgetWithWiki"""
    def __init__(self, date=None):
        super().__init__(date)
        # logger.debug('Setting up the custom tooltip')
        m = self.get_months()[self.date.month-1]
        d = self.date.strftime('%d')
        self.title = '{d}_{m}'.format(m=m, d=d)
        self.worker = Executor.submit(self.setup_date_event)

    def setup_date_event(self):
        try:
            self.event = Gtk.Label()
            self.event.set_line_wrap(True)
            self.pack_start(self.event, True, True, 10)
            # text = self.date.strftime(self.date_format)
            # self.event.set_markup("<span size='large'>"+text+'</span>')
            url = 'https://www.google.com/calendar/ical/en.ir%23holiday%40group.v.calendar.google.com/public/basic.ics'
            cal = loadics(url)
            tooltip = ''
            date = date_to_georgian(self.date)
            for component in cal.walk():
                if component.name == 'VEVENT':
                    vdate = component.get('dtstart').dt
                    if vdate.year == date.year and vdate.month == date.month \
                            and vdate.day == date.day:
                        tooltip = str(component.get('summary', ''))
            # text = self.date.strftime(self.date_format)
            # markup = "<span size='large'>" + text + "</span>"
            self.event.set_markup(tooltip)
            # self.big_day.set_tooltip_markup(tooltip[:200])
        except Exception:
            logger.exception(Exception)


class IcsListTreeView(Gtk.TreeView):
    """docstring for IcsListTreeView
     a Gtk.TreeView for displaying the ics event list"""
    def __init__(self, win):
        super().__init__()
        self.win = win
    def create_list_model(self):
        # enabled, editable, description, path
        self.store = Gtk.ListStore(bool, bool, str, str)
    def add_defaults_to_model(self):
        self.store.append(
            [True, False, 'Holidays of Iran',
             'https://www.google.com/calendar/ical/en.ir%23holi' +
                'day%40group.v.calendar.google.com/public/basic.ics'])
    def from_settings(self):
        

class IcsEvents(IPlugin):
    """
    ICS events Plugin

    can add a list of .ics files to your calendar.

    """
    def __init__(self):
        # Make sure to call the parent class (`IPlugin`) methods when
        # overriding them.
        super().__init__()

        # The `app` property was added to the manager singleton instance when
        # the manager was setup. See ExampleApp.__init__() in the
        # yapsy-gtk-example.py file.
        manager = PluginManagerSingleton.get()
        self.parent = manager.parent

    def activate(self):
        # Make sure to call `activate()` on the parent class to ensure that the
        # `is_activated` property gets set.
        super().activate()
        day_widgets = self.parent.day_widgets
        for i, day_widget in enumerate(day_widgets):
            # if isinstance(day_widget, GeorgianDayWidget):
            #     logger.debug('replacing GeorgianDayWidget(s)')
            #     day_widgets[i] = GeorgianDayWidgetWithWiki(day_widget.date)
            if isinstance(day_widget, PersianDayWidget):
                logger.debug('replacing PersianDayWidget(s)')
                day_widgets[i] = PersianDayWidgetWithWiki(day_widget.date)
        self.parent.handler.update_everything()

    def deactivate(self):
        # Make sure to call `deactivate()` on the parent class to ensure that
        # the `is_activated` property gets set.
        super().deactivate()
        day_widgets = self.parent.day_widgets
        for i, day_widget in enumerate(day_widgets):
            # if isinstance(day_widget, GeorgianDayWidgetWithWiki):
            #     day_widgets[i] = GeorgianDayWidget(day_widget.date)
            if isinstance(day_widget, PersianDayWidgetWithWiki):
                day_widgets[i] = PersianDayWidget(day_widget.date)
        self.parent.handler.update_everything()
