#!/usr/bin/env python3
from gi.repository import Gtk, GLib
import khayyam
import datetime

from calendar_widget import PersianCalendarWidget, GeorgianCalendarWidget
from day_widget import PersianDayWidget, GeorgianDayWidget
from events_handler import EventsHandler

# get the full path of the file
import os
import sys
if os.path.dirname(sys.argv[0]) != '.':
    if sys.argv[0][0] == '/':
        FULL_PATH = os.path.dirname(sys.argv[0])
    else:
        FULL_PATH = os.getcwd() + '/' + os.path.dirname(sys.argv[0])
else:
    FULL_PATH = os.getcwd()


class MainWindow(Gtk.Window):

    def __init__(self, date=None):
        super().__init__(title='گاه شمار')
        if date is None:
            date = datetime.date.today()
        self.date = date

        self.full_path = FULL_PATH

        pday = PersianDayWidget()
        gday = GeorgianDayWidget()
        self.day_widgets = [pday, gday]

        pcal = PersianCalendarWidget(khayyam.JalaliDate.from_date(date))
        pcal.parent = self
        gcal = GeorgianCalendarWidget(date)
        gcal.parent = self
        self.calendars = [pcal, gcal]
        self.handler = EventsHandler(self)

        self.main_grid = Gtk.Grid()
        main_grid = self.main_grid
        self.add(main_grid)
        main_grid.set_column_homogeneous(True)
        main_grid.set_column_spacing(spacing=20)
        # main_grid.set_row_homogeneous(True)
        main_grid.set_row_spacing(spacing=20)

        self.draw_interface()

        # update interface every 5 seconds
        GLib.timeout_add_seconds(5, self.handler.update_everything)

    def draw_interface(self):
        main_grid = self.main_grid
        for i, v in enumerate(self.day_widgets):
            main_grid.attach(v, i, 0, 1, 1)
        for i, v in enumerate(self.calendars):
            main_grid.attach(v, i, 1, 1, 1)
        self.setup_header_bar()

    def setup_header_bar(self):
        # set header bar
        hb = Gtk.HeaderBar()
        hb.props.show_close_button = True
        hb.props.title = 'گاه شمار'
        button = Gtk.Button(label='امروز')
        button.connect("clicked", self.set_today)
        hb.pack_start(button)
        self.set_titlebar(hb)

    def set_today(self, *args):
        self.handler.update_everything(datetime.date.today())

if __name__ == '__main__':
    win = MainWindow()
    win.connect("delete-event", Gtk.main_quit)
    win.set_icon_name("calendar")
    win.show_all()
    Gtk.main()
