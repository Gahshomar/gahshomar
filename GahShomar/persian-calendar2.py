#!/usr/bin/env python3
from os.path import join, split
from gi.repository import Gtk, Gio, GdkPixbuf
import khayyam
import datetime

from calendar_widget import PersianCalendarWidget, GeorgianCalendarWidget
from day_widget import PersianDayWidget, GeorgianDayWidget
from events_handler import EventsHandler


class MainWindow(Gtk.Window):

    def __init__(self, date=None):
        super().__init__(title='گاه شمار')
        if date is None:
            date = datetime.date.today()
        self.date = date

        pday = PersianDayWidget()
        gday = GeorgianDayWidget()
        self.day_widgets = [gday, pday]

        pcal = PersianCalendarWidget(khayyam.JalaliDate.from_date(date))
        pcal.parent = self
        gcal = GeorgianCalendarWidget(date)
        gcal.parent = self
        self.calendars = [gcal, pcal]
        self.handler = EventsHandler(self)

        self.main_grid = Gtk.Grid()
        main_grid = self.main_grid
        self.add(main_grid)
        main_grid.set_column_homogeneous(True)
        main_grid.set_column_spacing(spacing=20)
        # main_grid.set_row_homogeneous(True)
        main_grid.set_row_spacing(spacing=20)

        self.draw_interface()

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
        button = Gtk.Button()
        path = split(__file__)[0]
        name = '../data/icons/ubuntu-mono-light/persian-calendar-{}.png'
        name = name.format(khayyam.JalaliDate.today().day)
        path = join(path, name)
        pixbuf = GdkPixbuf.Pixbuf.new_from_file(path)
        scale = 15
        print(513//scale)
        pixbuf = pixbuf.scale_simple(475//scale, 513//scale, GdkPixbuf.InterpType.BILINEAR)
        image = Gtk.Image.new_from_pixbuf(pixbuf)
        # image.set_pixel_size(1)
        # image.set_pixel_size(Gtk.IconSize.LARGE_TOOLBAR)
        # icon = Gio.ThemedIcon(name="go-home")
        # image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.LARGE_TOOLBAR)
        button.add(image)
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
