# -*- Mode: Python; coding: utf-8; indent-tabs-mode: s; tab-width: 4 -*-

from gi.repository import Gtk
from .gi_composites import GtkTemplate
from .widgets import DayWidget, MonthsWidget, CalendarWidget
from .calendar import GREGORIAN_DATE, PERSIAN_DATE


@GtkTemplate(ui='/org/gnome/Gahshomar/window.ui')
class GahshomarWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'GahshomarWindow'

    header_bar = GtkTemplate.Child()
    today_button = GtkTemplate.Child()
    grid = GtkTemplate.Child()
    persian_box = GtkTemplate.Child()
    gregorian_box = GtkTemplate.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.init_template()

        # Add day widgets
        # GtkBox.pack_start(child, expand, fill, padding)
        self.persian_day = DayWidget()
        self.gregorian_day = DayWidget()
        self.persian_box.pack_start(self.persian_day, True, True, 0)
        self.gregorian_box.pack_start(self.gregorian_day, True, True, 0)

        # Add calendar widgets
        self.persian_calendar = CalendarWidget()
        self.gregorian_calendar = CalendarWidget()
        self.persian_box.pack_start(self.persian_calendar, True, True, 0)
        self.gregorian_box.pack_start(self.gregorian_calendar, True, True, 0)

        # Add month widgets
        self.persian_month = MonthsWidget()
        self.gregorian_month = MonthsWidget()
        self.persian_calendar.popover.add(self.persian_month)
        self.gregorian_calendar.popover.add(self.gregorian_month)
