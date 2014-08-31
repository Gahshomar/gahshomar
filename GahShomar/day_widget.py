#!/usr/bin/python
from gi.repository import Gtk

from my_calendar import PersianCalendar, GeorgianCalendar


class DayWidget(Gtk.Box):
    """docstring for DayWidget"""
    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL)
        # self.destroy()
        self.setup_big_day()
        self.setup_date()

    def setup_big_day(self):
        day = Gtk.Label()
        self.pack_start(day, True, True, 10)
        text = self.date.strftime('%d')
        day.set_markup("<span size='xx-large'>"+text+'</span>')

    def setup_date(self):
        day = Gtk.Label()
        self.pack_start(day, True, True, 10)
        text = self.date.strftime(self.date_format)
        day.set_markup("<span size='large'>"+text+'</span>')




class PersianDayWidget(DayWidget, PersianCalendar):
    """docstring for PersianDayWidget"""
    def __init__(self, date=None):
        PersianCalendar.__init__(self, date)
        self.date_format = '%A، %d %B %Y'
        DayWidget.__init__(self)


class GeorgianDayWidget(DayWidget, GeorgianCalendar):
    """docstring for GeorgianDayWidget"""
    def __init__(self, date=None):
        GeorgianCalendar.__init__(self, date)
        self.date_format = '%A, %d %B %Y'
        DayWidget.__init__(self)
