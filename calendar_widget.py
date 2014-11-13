#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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

from gi.repository import Gtk, Gio

from my_calendar import PersianCalendar, GeorgianCalendar, date_to_georgian,\
    add_months, add_years
from months_widget import PersianMonthsWidget, GeorgianMonthsWidget


class CalendarWidget(Gtk.Box):
    """docstring for CalendarWidget"""
    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL)
        # self.set_border_width(10)
        # self.set_size_request(400, -1)
        self.setup_header()
        self.setup_tobbar()
        self.setup_grid()
        # self.setup_tobbar()
        self.connect_date_buttons()
        self.connect_month_arrow()
        self.connect_year_arrow()

    def setup_year_entry(self):
        self.header.year = Gtk.Entry()
        self.header.year.set_text(self.date.strftime('%Y'))
        year = self.header.year
        year.set_icon_from_gicon(Gtk.EntryIconPosition.PRIMARY,
                                 Gio.ThemedIcon(name='list-remove-symbolic'))
        year.set_icon_from_gicon(Gtk.EntryIconPosition.SECONDARY,
                                 Gio.ThemedIcon(name='list-add-symbolic'))
        year.set_icon_activatable(Gtk.EntryIconPosition.PRIMARY, True)
        year.set_icon_activatable(Gtk.EntryIconPosition.SECONDARY, True)

    def setup_month_popup(self):
        months = list(self.get_months())
        month_label = months[self.date.month-1]
        self.header.month = Gtk.Button(label=month_label)
        self.header.month.set_size_request(150, -1)
        self.header.pack_start(self.header.month, False, True, 0)
        self.header.month.connect('clicked',
                                  self.display_months, self.date)

    def display_months(self, *args):
        date = args[-1]
        win = Gtk.Window(Gtk.WindowType.TOPLEVEL)  # POPUP or TOPLEVEL
        win.set_transient_for(self.parent)
        months = self.MonthWidget(date)
        win.add(months)
        win.set_position(Gtk.WindowPosition.MOUSE)
        win.set_decorated(False)
        win.connect('focus-out-event', self.destroy_months_win)
        self.month_widget = months
        self.month_widget_win = win
        self.connect_month_buttons()
        win.show_all()

    def destroy_months_win(self, *args):
        self.month_widget_win.destroy()

    def connect_month_buttons(self):
        months = self.month_widget
        button_list = months.grid.button_list
        for button, _, i in button_list:
            button.connect("clicked",
                           self.month_button_pressed, i, months.date)

    def month_button_pressed(self, *args):
        month, date = args[-2:]
        date = date.replace(month=month)
        date = date_to_georgian(date)
        self.month_widget_win.close()
        self.parent.handler.update_everything(date)

    def setup_header(self):
        self.header = Gtk.Box()
        self.pack_start(self.header, False, False, 5)
        # month buttons
        if self.rtl:
            rtlt = ('next', 'previous')
        else:
            rtlt = ('previous', 'next')
        btl = Gtk.Button.new_from_icon_name('go-{}-symbolic'.format(rtlt[1]), 0)
        btr = Gtk.Button.new_from_icon_name('go-{}-symbolic'.format(rtlt[0]), 0)
        self.header.btl = btl
        self.header.btr = btr
        if self.rtl:
            self.header.pack_start(btl, False, False, 0)
        else:
            self.header.pack_start(btr, False, False, 0)
        # months
        self.setup_month_popup()
        if self.rtl:
            self.header.pack_start(btr, False, False, 0)
        else:
            self.header.pack_start(btl, False, False, 0)
        # years
        self.setup_year_entry()
        self.header.pack_end(self.header.year, False, True, 0)

    def setup_tobbar(self):
        self.topbarbox = Gtk.Box()
        self.topbarbox.set_homogeneous(True)
        # self.topbarbox.override_background_color(Gtk.StateFlags.NORMAL,
        #                                          Gdk.RGBA(red=74/255,
        #                                                   green=144/255,
        #                                                   blue=217/255))
        self.pack_start(self.topbarbox, False, True, 10)
        # self.pack_start(Gtk.HSeparator(), False, False, 0)
        rtl = -1 if self.rtl else 1
        week_days = self.get_week_days()[::rtl]
        # print(week_days, rtl)
        for i, (week_day, tooltip) in enumerate(week_days):
            label = Gtk.Label(None)
            label.set_markup(
                "<span foreground='#4A90D9'>" +  # background='#4A90D9'
                week_day + '</span>')
            label.set_tooltip_markup(tooltip)
            # label.set_halign(Gtk.Align.CENTER)
            # label.override_color(Gtk.StateFlags.NORMAL,
            #     Gdk.RGBA(red=0, green=0, blue=1.0, alpha=1.0))
            self.topbarbox.pack_start(label, True, True, 0)
            # self.grid.attach(label, i, 0, 1, 1)
        # self.grid.override_background_color(
        #     Gtk.StateFlags.NORMAL, Gdk.RGBA(
        #         red=74/255, green=144/255, blue=217/255))

    def setup_grid(self):
        self.gen_grid_mat()
        self.grid = Gtk.Grid()
        self.pack_start(self.grid, True, True, 0)
        self.grid.set_column_homogeneous(True)
        self.grid.set_column_spacing(spacing=0)
        self.grid.set_row_homogeneous(True)
        self.grid.set_row_spacing(spacing=0)
        # self.grid.connect('set-focus-child', self.grid_pressed, None)
        self.grid.button_list = []
        for j, row in enumerate(self.grid_mat):
            for i, (date, day) in enumerate(row):
                label = Gtk.Label()
                label.set_markup(day)
                button = Gtk.Button()
                button.set_image(label)
                button.set_relief(Gtk.ReliefStyle.NONE)
                button.date = date
                if date == self.date:
                    # button.override_color(Gtk.StateFlags.ACTIVE,
                    #                       Gdk.RGBA(red=0, green=0))
                    button.set_relief(Gtk.ReliefStyle.HALF)
                # button.connect("clicked",
                #                self.grid_pressed, (i, j, date))
                self.grid.attach(button, i, j+1, 1, 1)
                self.grid.button_list.append((button, date, i, j))

    def connect_date_buttons(self):
        button_list = self.grid.button_list
        for button, date, i, j in button_list:
            button.connect("clicked",
                           self.date_button_pressed, (i, j, date))

    def date_button_pressed(self, *args):
        date = date_to_georgian(args[-1][-1])
        self.parent.handler.update_everything(date)

    def connect_year_arrow(self):
        self.header.year.connect("icon-press",
                                 self.year_arrow_pressed)
        self.header.year.connect('activate',
                                 self.year_entered, self.date)

    def year_entered(self, yearEntry, date):
        year = yearEntry.get_text()
        try:
            year = int(year)
        except Exception:
            year = date.year
        date = date_to_georgian(date.replace(year=year))
        self.parent.handler.update_everything(date)

    def year_arrow_pressed(self, yera, icon_pos, event):
        if icon_pos == Gtk.EntryIconPosition.PRIMARY:
            date = add_years(self.parent.date, -1)
        else:
            date = add_years(self.parent.date, 1)
        self.parent.handler.update_everything(date)

    def connect_month_arrow(self):
        # left arrow
        self.header.btl.connect("clicked",
                                self.month_arrow_pressed, 'l')
        # right arrow
        self.header.btr.connect("clicked",
                                self.month_arrow_pressed, 'r')

    def month_arrow_pressed(self, *args):
        l_r = args[-1]
        if l_r == 'r':
            date = add_months(self.parent.date, -1)
        else:
            date = add_months(self.parent.date, 1)
        self.parent.handler.update_everything(date)


class PersianCalendarWidget(CalendarWidget, PersianCalendar):
    """docstring for PersianCalendarWidget"""
    def __init__(self, date=None, rtl=True):
        PersianCalendar.__init__(self, date)
        self.rtl = rtl
        self.MonthWidget = PersianMonthsWidget
        CalendarWidget.__init__(self)


class GeorgianCalendarWidget(CalendarWidget, GeorgianCalendar):
    """docstring for GeorgianCalendarWidget"""
    def __init__(self, date=None, rtl=False):
        GeorgianCalendar.__init__(self, date)
        self.rtl = rtl
        self.MonthWidget = GeorgianMonthsWidget
        CalendarWidget.__init__(self)
