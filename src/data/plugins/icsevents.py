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
Executor = ThreadPoolExecutor(max_workers=4)
import urllib

# third-party library imports
from yapsy.IPlugin import IPlugin
from yapsy.PluginManager import PluginManagerSingleton
from gi.repository import Gtk, Gdk, GObject
try:
    from icalendar import Calendar
except ImportError:
    logger.error('icalendar python package needs to be installed', exc_info=1)
    raise

# local imports
from GahShomar.gs_calendar_widget import PersianCalendarWidget, GeorgianCalendarWidget
from GahShomar.gs_calendar import date_to_georgian
from GahShomar.gs_util import cache, debug


@cache
def loadics(url):
    if url.startswith('/'):
        path = url
    else:
        (path, message) = urllib.request.urlretrieve(url)
    with open(path, 'rb') as f:
        cal = Calendar.from_ical(f.read())
    return cal


class PersianCalendarWidgetEvent(PersianCalendarWidget):
    """docstring for PersianCalendarWidgetEvent"""
    def __init__(self, date=None, store=None):
        super().__init__(date)
        self.worker = Executor.submit(self.loadicslist)

    def gen_grid_mat(self):
        super().gen_grid_mat()
        # for j, row in enumerate(self.grid_mat):
        #     for i, (date, text) in enumerate(row):


        # # decide if it is going to be 6 rows or 5
        # if self.first_day_of_month + self.days_in_month > 35:
        #     rows = 6
        # else:
        #     rows = 5

        # self.grid_mat = []  # 5 or 6 row, 7 column
        # for _ in range(rows):
        #     row = []
        #     for _ in range(7):
        #         row.append([])
        #     self.grid_mat.append(row)
        # delta = - (self.first_day_of_month + self.date.day) + 1
        # # print(delta)
        # for j in range(rows):
        #     for i in range(7):
        #         if self.rtl:
        #             delta_time = datetime.timedelta(days=6-i+j*7+delta)
        #         else:
        #             delta_time = datetime.timedelta(days=i+j*7+delta)
        #         date = self.date+delta_time
        #         if date.month == self.date.month:
        #             text = '<span fgcolor="black">{}</span>'
        #         else:
        #             text = '<span fgcolor="gray">{}</span>'
        #         self.grid_mat[j][i] = (date, text.format(date.strftime('%d')))


# class PersianDayWidgetWithWiki(PersianDayWidget):
#     """docstring for PersianDayWidgetWithWiki"""
#     def __init__(self, date=None):
#         super().__init__(date)
#         # logger.debug('Setting up the custom tooltip')
#         m = self.get_months()[self.date.month-1]
#         d = self.date.strftime('%d')
#         self.title = '{d}_{m}'.format(m=m, d=d)
#         self.worker = Executor.submit(self.setup_date_event)

#     def setup_date_event(self):
#         try:
#             self.event = Gtk.Label()
#             self.event.set_line_wrap(True)
#             self.pack_start(self.event, True, True, 10)
#             # text = self.date.strftime(self.date_format)
#             # self.event.set_markup("<span size='large'>"+text+'</span>')
#             url = 'https://www.google.com/calendar/ical/en.ir%23holiday%40group.v.calendar.google.com/public/basic.ics'
#             cal = loadics(url)
#             tooltip = ''
#             date = date_to_georgian(self.date)
#             for component in cal.walk():
#                 if component.name == 'VEVENT':
#                     vdate = component.get('dtstart').dt
#                     if vdate.year == date.year and vdate.month == date.month \
#                             and vdate.day == date.day:
#                         tooltip = str(component.get('summary', ''))
#             # text = self.date.strftime(self.date_format)
#             # markup = "<span size='large'>" + text + "</span>"
#             self.event.set_markup(tooltip)
#             # self.big_day.set_tooltip_markup(tooltip[:200])
#         except Exception:
#             logger.exception(Exception)


class CellRendererColorButton(Gtk.CellRenderer):
    __gsignals__ = {
        'color-set': (GObject.SIGNAL_RUN_FIRST, None, (str,))
    }

    # def do_color_set(self, color):
    #     print "class method for `my_signal' called with argument", arg

    color = GObject.property(type=str, default='rgb(0,0,255)')

    def __init__(self):
        super().__init__()

    def do_set_property(self, pspec, value):
        setattr(self, pspec.name, value)

    def do_get_property(self, pspec):
        return getattr(self, pspec.name)

    # @debug
    def do_get_size(self, widget, cell_area):
        # FIXME: get_size() doc's say it's deprectated,
        # but do_get_preferred_size does not seem to work yet.
        color1 = Gdk.RGBA()
        succeed = color1.parse(self.color)
        if not succeed:
            color1.parse('rgb(0,0,255)')
        button = Gtk.ColorButton.new_with_rgba(color1)
        button.connect('color-set', self._on_color_set)
        self.button = button
        minimum_height, natural_height, minimum_baseline, natural_baseline = \
            button.get_preferred_height_and_baseline_for_width(-1)
        return (0, 0, natural_baseline, natural_height)

    @debug
    def do_render(self, cr, widget, background_area, cell_area, flags):
        # selected = (flags & Gtk.CellRendererState.SELECTED) != 0
        # prelit = (flags & Gtk.CellRendererState.PRELIT) != 0
        x, y, buttonWidth, buttonHeight = self.get_size(widget, cell_area)
        print(x, y, buttonWidth, buttonHeight)
        # root_window = button.get_root_window()
        cr.set_line_width(10)
        # red
        cr.set_source_rgba(0.5, 0.0, 0.0, 1.0)

        # get the width and height of the drawing area
        w, h = buttonWidth, buttonHeight
        # w = self.darea.get_allocated_width()
        # h = self.darea.get_allocated_height()

        # move to the center of the drawing area
        # (translate from the top left corner to w/2, h/2)
        cr.translate(w / 2, h / 2)
        # draw a line to (55, 0)
        cr.line_to(55, 0)
        # and get back to (0, 0)
        cr.line_to(0, 0)
        # draw an arc centered in the origin, 50 pixels wide, from the angle 0
        # (in radians) to the angle given by the spinbutton (in degrees)
        import math
        cr.arc(0, 0, 50, 0, 270 * (math.pi / 180))
        # draw a line back to the origin
        cr.line_to(0, 0)
        # drawing the path, and keeping the path for future use
        cr.stroke_preserve()

        # set a colour
        cr.set_source_rgba(0.0, 0.5, 0.5, 1.0)
        # and use it to fill the path (that we had kept)
        cr.fill()
        # y = cell_area.y + 10
        # x = cell_area.width + 20
        # Gdk.cairo_set_source_window(cr, root_window, x, y)
        # style = widget.get_style()
        # style.paint_box(
        #     cr, widget.get_state(), Gtk.SHADOW_ETCHED_OUT,
        #     None, widget, None, 0, 0, buttonWidth, buttonHeight)
        # return True
    # def do_activate(self, event, widget, path, background_area, cell_area,
    #                 flags):
    #     pass

    def _on_color_set(self, button, data=None):
        self.emit("color-set", button.get_rgba().to_string())


class IcsListTreeView(Gtk.Box):
    """a Gtk.TreeView for displaying the ics event list"""
    def __init__(self, win):
        super().__init__(orientation=Gtk.Orientation.VERTICAL)
        self.win = win
        self.create_list_model()
        self.add_defaults_to_model()
        self.tree = Gtk.TreeView(self.store)
        self.add_model_to_tree()
        select = self.tree.get_selection()
        select.set_mode(Gtk.SelectionMode.BROWSE)
        # select.connect("changed", self.on_tree_selection_changed)
        self.sw = Gtk.ScrolledWindow()
        self.sw.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.sw.add(self.tree)

        self.pack_start(self.sw, True, True, 0)
        self.show_all()

    def create_list_model(self):
        # enabled, editable, description, path, color
        self.store = Gtk.ListStore(bool, bool, str, str, str)

    def add_model_to_tree(self):
        renderer = Gtk.CellRendererToggle()
        renderer.connect('toggled', self._on_active_toggled)
        column = Gtk.TreeViewColumn("Enable", renderer, active=0)
        self.tree.append_column(column)

        renderer = Gtk.CellRendererText()
        renderer.connect('edited', self._on_description_edited)
        column = Gtk.TreeViewColumn("Description", renderer, text=2, editable=1)
        self.tree.append_column(column)

        renderer = CellRendererColorButton()
        renderer.connect('color-set', self._on_color_changed)
        column = Gtk.TreeViewColumn("Color", renderer, color=4)
        self.tree.append_column(column)

        renderer = Gtk.CellRendererText()
        renderer.connect('edited', self._on_url_edited)
        column = Gtk.TreeViewColumn("Path/Url", renderer, text=3, editable=1)
        self.tree.append_column(column)

    def add_defaults_to_model(self):
        self.store.append(
            [True, False, 'Holidays of Iran',
             'https://www.google.com/calendar/ical/en.ir%23holi' +
                'day%40group.v.calendar.google.com/public/basic.ics', 'blue'])
        self.store.append([False, True, '', '', ''])

    def from_settings(self):
        if 'IcsEvents' in self.win.config:
            if 'list' in self.win.config['IcsEvents']:
                icslist = self.win.config['IcsEvents']['list']
                d = locals()
                exec('icslist = ' + icslist, globals(), d)
                icslist = d['icslist']
                self.store.extend(icslist)

    def _on_active_toggled(self, cell, path, data=None):
        # toggle the check box
        iter1 = self.store.get_iter(path)
        self.store[iter1][0] = not self.store[iter1][0]

    def _on_description_edited(self, cell, path, text):
        iter1 = self.store.get_iter(path)
        self.store[iter1][2] = text
        if self.store[-1][2] != '' or self.store[-1][3] != '':
            self.store.append([False, True, '', ''])

    def _on_url_edited(self, cell, path, text):
        iter1 = self.store.get_iter(path)
        self.store[iter1][3] = text
        if self.store[-1][2] != '' or self.store[-1][3] != '':
            self.store.append([False, True, '', ''])

    def _on_color_changed(self, cell, path, color, data=None):
        iter1 = self.store.get_iter(path)
        self.store[iter1][4] = color


class IcsEvents(IPlugin):
    """
    ICS events Plugin

    can add a list of .ics files to your calendar.

    """
    def __init__(self):
        # Make sure to call the parent class (`IPlugin`) methods when
        # overriding them.
        super().__init__()

        manager = PluginManagerSingleton.get()
        self.parent = manager.parent

    def activate(self):
        # Make sure to call `activate()` on the parent class to ensure that the
        # `is_activated` property gets set.
        super().activate()
        self.icslisttreeview = IcsListTreeView(self.parent)
        nb = self.parent.gs_settings_win.notebook_settings
        self.nbindex = nb.append_page(
            self.icslisttreeview, Gtk.Label('Events'))
        nb.show_all()
        # self.parent.main_grid.attach(
        #     self.icslisttreeview, 3, 0, 1, 2)
        # day_widgets = self.parent.day_widgets
        # for i, day_widget in enumerate(day_widgets):
        #     # if isinstance(day_widget, GeorgianDayWidget):
        #     #     logger.debug('replacing GeorgianDayWidget(s)')
        #     #     day_widgets[i] = GeorgianDayWidgetWithWiki(day_widget.date)
        #     if isinstance(day_widget, PersianDayWidget):
        #         logger.debug('replacing PersianDayWidget(s)')
        #         day_widgets[i] = PersianDayWidgetWithWiki(day_widget.date)
        # self.parent.handler.update_everything()

    def deactivate(self):
        # Make sure to call `deactivate()` on the parent class to ensure that
        # the `is_activated` property gets set.
        super().deactivate()
        nb = self.parent.gs_settings_win.notebook_settings
        nb.remove_page(self.nbindex)
        nb.show_all()
        # self.parent.main_grid.remove_column(3)

        # day_widgets = self.parent.day_widgets
        # for i, day_widget in enumerate(day_widgets):
        #     # if isinstance(day_widget, GeorgianDayWidgetWithWiki):
        #     #     day_widgets[i] = GeorgianDayWidget(day_widget.date)
        #     if isinstance(day_widget, PersianDayWidgetWithWiki):
        #         day_widgets[i] = PersianDayWidget(day_widget.date)
        # self.parent.handler.update_everything()
