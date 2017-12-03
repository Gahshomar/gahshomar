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

from gi.repository import Gtk
from .gi_composites import GtkTemplate


@GtkTemplate(ui='/org/gnome/Gahshomar/day-widget.ui')
class DayWidget(Gtk.Box):
    __gtype_name__ = 'DayWidget'

    label = GtkTemplate.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.init_template()


@GtkTemplate(ui='/org/gnome/Gahshomar/months-widget.ui')
class MonthsWidget(Gtk.Box):
    __gtype_name__ = 'MonthsWidget'

    grid = GtkTemplate.Child()
    button1 = GtkTemplate.Child()
    button2 = GtkTemplate.Child()
    button3 = GtkTemplate.Child()
    button4 = GtkTemplate.Child()
    button5 = GtkTemplate.Child()
    button6 = GtkTemplate.Child()
    button7 = GtkTemplate.Child()
    button8 = GtkTemplate.Child()
    button9 = GtkTemplate.Child()
    button10 = GtkTemplate.Child()
    button11 = GtkTemplate.Child()
    button12 = GtkTemplate.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.init_template()


@GtkTemplate(ui='/org/gnome/Gahshomar/calendar-widget.ui')
class CalendarWidget(Gtk.Box):
    __gtype_name__ = 'CalendarWidget'

    month_year_header = GtkTemplate.Child()
    month_menu_button = GtkTemplate.Child()
    month_label = GtkTemplate.Child()
    year_entry = GtkTemplate.Child()
    week_days = GtkTemplate.Child()
    week_day1 = GtkTemplate.Child()
    week_day2 = GtkTemplate.Child()
    week_day3 = GtkTemplate.Child()
    week_day4 = GtkTemplate.Child()
    week_day5 = GtkTemplate.Child()
    week_day6 = GtkTemplate.Child()
    week_day7 = GtkTemplate.Child()
    days_grid = GtkTemplate.Child()
    button1 = GtkTemplate.Child()
    button2 = GtkTemplate.Child()
    button3 = GtkTemplate.Child()
    button4 = GtkTemplate.Child()
    button5 = GtkTemplate.Child()
    button6 = GtkTemplate.Child()
    button7 = GtkTemplate.Child()
    button8 = GtkTemplate.Child()
    button9 = GtkTemplate.Child()
    button10 = GtkTemplate.Child()
    button11 = GtkTemplate.Child()
    button12 = GtkTemplate.Child()
    button13 = GtkTemplate.Child()
    button14 = GtkTemplate.Child()
    button15 = GtkTemplate.Child()
    button16 = GtkTemplate.Child()
    button17 = GtkTemplate.Child()
    button18 = GtkTemplate.Child()
    button19 = GtkTemplate.Child()
    button20 = GtkTemplate.Child()
    button21 = GtkTemplate.Child()
    button22 = GtkTemplate.Child()
    button23 = GtkTemplate.Child()
    button24 = GtkTemplate.Child()
    button25 = GtkTemplate.Child()
    button26 = GtkTemplate.Child()
    button27 = GtkTemplate.Child()
    button28 = GtkTemplate.Child()
    button29 = GtkTemplate.Child()
    button30 = GtkTemplate.Child()
    button31 = GtkTemplate.Child()
    button32 = GtkTemplate.Child()
    button33 = GtkTemplate.Child()
    button34 = GtkTemplate.Child()
    button35 = GtkTemplate.Child()
    button36 = GtkTemplate.Child()
    button37 = GtkTemplate.Child()
    button38 = GtkTemplate.Child()
    button39 = GtkTemplate.Child()
    button40 = GtkTemplate.Child()
    button41 = GtkTemplate.Child()
    button42 = GtkTemplate.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.init_template()
