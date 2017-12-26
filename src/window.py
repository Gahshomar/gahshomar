# -*- Mode: Python; coding: utf-8; indent-tabs-mode: s; tab-width: 4 -*-

from gi.repository import Gtk
from .gi_composites import GtkTemplate
from .widgets import DayWidget, MonthsWidget, CalendarWidget
from .calendar import GREGORIAN_DATE, PERSIAN_DATE, TODAY


@GtkTemplate(ui='/org/gahshomar/Gahshomar/window.ui')
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
        self.calendar = GREGORIAN_DATE
        self.calendar.connect("notify::date", self.update)
        # we need to update the today button when today changes
        TODAY.connect("notify::date", self.update)

        # Add day widgets
        # GtkBox.pack_start(child, expand, fill, padding)
        self.persian_day = DayWidget(PERSIAN_DATE)
        self.gregorian_day = DayWidget(GREGORIAN_DATE)
        self.persian_box.pack_start(self.persian_day, True, True, 0)
        self.gregorian_box.pack_start(self.gregorian_day, True, True, 0)

        # Add calendar widgets
        self.persian_calendar = CalendarWidget(GREGORIAN_DATE, PERSIAN_DATE)
        self.gregorian_calendar = CalendarWidget(GREGORIAN_DATE,
                                                 GREGORIAN_DATE)
        self.persian_box.pack_start(self.persian_calendar, True, True, 0)
        self.gregorian_box.pack_start(self.gregorian_calendar, True, True, 0)

        # Add month widgets
        self.persian_month = MonthsWidget(GREGORIAN_DATE, PERSIAN_DATE)
        self.gregorian_month = MonthsWidget(GREGORIAN_DATE, GREGORIAN_DATE)
        self.persian_calendar.popover.add(self.persian_month)
        self.gregorian_calendar.popover.add(self.gregorian_month)

        # the icon
        self.set_default_icon_name("org.gahshomar.Gahshomar")

        self.update()

    def update(self, *args):
        if self.calendar.date == self.calendar.today():
            self.today_button.set_sensitive(False)
        else:
            self.today_button.set_sensitive(True)

    @GtkTemplate.Callback
    def on_today_button_clicked(self, *args):
        self.calendar.date = self.calendar.today()
