# window.py
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

from gi.repository import Gtk
from .gi_composites import GtkTemplate
from .widgets import DayWidget, MonthsWidget, CalendarWidget


@GtkTemplate(ui='/org/gnome/Gahshomar/window.ui')
class GahshomarWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'GahshomarWindow'

    header_bar = GtkTemplate.Child()
    today_button = GtkTemplate.Child()
    main_grid = GtkTemplate.Child()
    persian_main_box = GtkTemplate.Child()
    gregorian_main_box = GtkTemplate.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.init_template()

        # Add day widgets
        # GtkBox.pack_start(child, expand, fill, padding)
        self.persian_day_widget = DayWidget()
        self.gregorian_day_widget = DayWidget()
        self.persian_main_box.pack_start(
            self.persian_day_widget, True, True, 0)
        self.gregorian_main_box.pack_start(
            self.gregorian_day_widget, True, True, 0)

        # Add calendar widgets
        self.persian_calendar_widget = CalendarWidget()
        self.gregorian_calendar_widget = CalendarWidget()
        self.persian_main_box.pack_start(
            self.persian_calendar_widget, True, True, 0)
        self.gregorian_main_box.pack_start(
            self.gregorian_calendar_widget, True, True, 0)

        # Add month widgets
        self.persian_month_widget = MonthsWidget()
        self.gregorian_month_widget = MonthsWidget()
