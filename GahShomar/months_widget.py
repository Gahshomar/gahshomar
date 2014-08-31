#!/usr/bin/python
from gi.repository import Gtk

from my_calendar import PersianCalendar, GeorgianCalendar


class MonthsWidget(Gtk.Box):
    """docstring for MonthsWidget"""
    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL)
        # self.destroy()
        # self.setup_years()
        self.setup_grid()

    def setup_grid(self):
        self.grid = Gtk.Grid()
        self.pack_start(self.grid, False, True, 0)
        self.grid.set_column_homogeneous(True)
        self.grid.set_column_spacing(spacing=10)
        self.grid.set_row_homogeneous(True)
        self.grid.set_row_spacing(spacing=10)
        self.grid.button_list = []
        for i, month in enumerate(self.get_months()):
            button = Gtk.Button(label=month)
            if i+1 == self.date.month:
                button.set_relief(Gtk.ReliefStyle.HALF)
            else:
                button.set_relief(Gtk.ReliefStyle.NONE)
            if self.rtl:
                self.grid.attach(button, 2 - i % 3, i // 3, 1, 1)
            else:
                self.grid.attach(button, i % 3, i // 3, 1, 1)
            self.grid.button_list.append((button, month, i+1))


class PersianMonthsWidget(MonthsWidget, PersianCalendar):
    """docstring for PersianMonthsWidget"""
    def __init__(self, date=None, rtl=True):
        PersianCalendar.__init__(self, date)
        self.rtl = rtl
        MonthsWidget.__init__(self)


class GeorgianMonthsWidget(MonthsWidget, GeorgianCalendar):
    """docstring for GeorgianMonthsWidget"""
    def __init__(self, date=None, rtl=False):
        GeorgianCalendar.__init__(self, date)
        self.rtl = rtl
        MonthsWidget.__init__(self)
