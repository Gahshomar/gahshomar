#!/usr/bin/env python3

from gi.repository import Gtk, Gdk, Gio

from my_calendar import PersianCalendar, GeorgianCalendar


class CalendarWidget(Gtk.Box):
    """docstring for CalendarWidget"""
    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL)
        # self.set_border_width(10)
        self.setup_header()
        self.setup_tobbar()
        self.setup_grid()

    def setup_year_entry(self):
        self.header.year = Gtk.Entry()
        self.header.year.set_text(self.date.strftime('%Y'))
        year = self.header.year
        year.set_icon_from_gicon(Gtk.EntryIconPosition.PRIMARY,
                                 Gio.ThemedIcon(name='list-remove'))
        year.set_icon_from_gicon(Gtk.EntryIconPosition.SECONDARY,
                                 Gio.ThemedIcon(name='list-add'))
        year.set_icon_activatable(Gtk.EntryIconPosition.PRIMARY, True)
        year.set_icon_activatable(Gtk.EntryIconPosition.SECONDARY, True)

    def setup_header(self):
        self.header = Gtk.Box()
        self.pack_start(self.header, False, False, 5)
        # month buttons
        btl = Gtk.Button.new_from_icon_name('list-add', 0)
        btr = Gtk.Button.new_from_icon_name('list-remove', 0)
        self.header.btl = btl
        self.header.btr = btr
        if self.rtl:
            self.header.pack_start(btl, False, False, 0)
        else:
            self.header.pack_start(btr, False, False, 0)
        # months
        self.header.month = Gtk.ComboBoxText()
        self.header.pack_start(self.header.month, False, True, 0)
        for i, month in enumerate(self.get_months()):
            self.header.month.append(str(i+1), month)
        self.header.month.set_active_id(str(self.date.month))
        if self.rtl:
            self.header.pack_start(btr, False, False, 0)
        else:
            self.header.pack_start(btl, False, False, 0)
        # years
        self.setup_year_entry()
        # self.header.year = Gtk.Label(label=self.date.strftime('%Y'))
        # # year buttons
        # btr = Gtk.Button.new_from_icon_name('list-add', 0)
        # btl = Gtk.Button.new_from_icon_name('list-remove', 0)
        # self.header.btly = btl
        # self.header.btry = btr

        # self.header.pack_end(self.header.btry, False, False, 0)
        self.header.pack_end(self.header.year, False, True, 0)
        # self.header.pack_end(self.header.btly, False, False, 0)

    def setup_tobbar(self):
        self.topbarbox = Gtk.Box()
        self.pack_start(self.topbarbox, False, True, 10)
        rtl = -1 if self.rtl else 1
        week_days = self.get_week_days()[::rtl]
        # print(week_days, rtl)
        for week_day in week_days:
            label = Gtk.Label(None)
            label.set_markup("<span foreground='#FFFFFF'>"+week_day+'</span>')
            # label.override_color(Gtk.StateFlags.NORMAL,
            #     Gdk.RGBA(red=0, green=0, blue=1.0, alpha=1.0))
            self.topbarbox.pack_start(label, True, True, 0)

        self.topbarbox.override_background_color(Gtk.StateFlags.NORMAL,
                                                 Gdk.RGBA(red=0, green=0))

    def setup_grid(self):
        self.gen_grid_mat()
        self.grid = Gtk.Grid()
        self.pack_start(self.grid, False, True, 0)
        self.grid.set_column_homogeneous(True)
        self.grid.set_column_spacing(spacing=10)
        self.grid.set_row_homogeneous(True)
        self.grid.set_row_spacing(spacing=10)
        # self.grid.connect('set-focus-child', self.grid_pressed, None)
        self.grid.button_list = []
        for j, row in enumerate(self.grid_mat):
            for i, (date, day) in enumerate(row):
                button = Gtk.Button(label=day)
                button.set_relief(Gtk.ReliefStyle.NONE)
                button.date = date
                if date == self.date:
                    # button.override_color(Gtk.StateFlags.ACTIVE,
                    #                       Gdk.RGBA(red=0, green=0))
                    button.set_relief(Gtk.ReliefStyle.HALF)
                # button.connect("button-press-event",
                #                self.grid_pressed, (i, j, date))
                self.grid.attach(button, i, j, 1, 1)
                self.grid.button_list.append((button, date, i, j))


class PersianCalendarWidget(CalendarWidget, PersianCalendar):
    """docstring for PersianCalendarWidget"""
    def __init__(self, date=None, rtl=True):
        PersianCalendar.__init__(self, date)
        self.rtl = rtl
        CalendarWidget.__init__(self)


class GeorgianCalendarWidget(CalendarWidget, GeorgianCalendar):
    """docstring for GeorgianCalendarWidget"""
    def __init__(self, date=None, rtl=False):
        GeorgianCalendar.__init__(self, date)
        self.rtl = rtl
        CalendarWidget.__init__(self)


class MainWindow(Gtk.Window):

    def __init__(self):
        super().__init__(title='Calendar Widgets')
        hbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        self.add(hbox)
        hbox.pack_start(PersianCalendarWidget(), True, True, 0)
        # hbox.pack_start(PersianCalendarWidget(rtl=False), True, True, 0)
        hbox.pack_start(GeorgianCalendarWidget(), True, True, 0)

if __name__ == '__main__':
    win = MainWindow()
    win.connect("delete-event", Gtk.main_quit)
    win.set_icon_name("calendar")
    win.show_all()
    Gtk.main()
