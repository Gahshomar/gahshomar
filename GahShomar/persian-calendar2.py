#!/usr/bin/env python3
from gi.repository import Gtk, Gio
import khayyam
import datetime

from my_calendar import add_months, add_years, date_to_georgian
from calendar_widget import PersianCalendarWidget, GeorgianCalendarWidget
from day_widget import PersianDayWidget, GeorgianDayWidget
from months_widget import PersianMonthsWidget, GeorgianMonthsWidget


class EventsHandler(object):
    """docstring for EventsHandler"""
    def __init__(self, parent):
        super().__init__()
        self.calendars = parent.calendars
        self.parent = parent
        for calendar in self.calendars:
            self.connect_all_buttons(calendar)
        for months in self.parent.months_widgets:
            self.connect_month_buttons(months)

    def update_calendars(self, date):
        self.parent.date = date
        # jdate = khayyam.JalaliDate.from_date(date)
        # update calendars
        for i, calendar in enumerate(self.calendars):
            if isinstance(calendar.date, khayyam.JalaliDate):
                # calendar.__init__(jdate)
                self.calendars[i] = PersianCalendarWidget(date)
            else:
                self.calendars[i] = GeorgianCalendarWidget(date)
                # calendar.__init__(gdate)
            self.connect_all_buttons(self.calendars[i])
            self.parent.vbox.remove(calendar)
            calendar.destroy()
            self.parent.vbox.pack_start(self.calendars[i], True, True, 0)
        self.update_day_widgets(date)
        self.update_months_widgets(date)
        self.parent.show_all()

    def update_day_widgets(self, date):
        for i, dayw in enumerate(self.parent.day_widgets):
            if isinstance(dayw.date, khayyam.JalaliDate):
                self.parent.day_widgets[i] = PersianDayWidget(date)
                # dayw.__init__(date)
            else:
                self.parent.day_widgets[i] = GeorgianDayWidget(date)
            self.parent.vbox2.remove(dayw)
            self.parent.vbox2.pack_start(self.parent.day_widgets[i], False,
                                         False, 0)

    def update_months_widgets(self, date):
        for i, monthsw in enumerate(self.parent.months_widgets):
            if isinstance(monthsw.date, khayyam.JalaliDate):
                self.parent.months_widgets[i] = PersianMonthsWidget(date)
            else:
                self.parent.months_widgets[i] = GeorgianMonthsWidget(date)
            self.parent.vbox3.remove(monthsw)
            self.parent.vbox3.pack_start(self.parent.months_widgets[i], False,
                                         False, 0)
            self.connect_month_buttons(self.parent.months_widgets[i])

    def connect_all_buttons(self, calendar):
        self.connect_date_buttons(calendar)
        self.connect_month_arrow(calendar)
        self.connect_month_combo(calendar)
        self.connect_year_arrow(calendar)

    def connect_year_arrow(self, calendar):
        calendar.header.year.connect("icon-press",
                                     self.year_arrow_pressed)
        calendar.header.year.connect('activate',
                                     self.year_entered, calendar.date)

    def year_entered(self, yearEntry, date):
        year = yearEntry.get_text()
        try:
            year = int(year)
        except Exception:
            year = date.year
        date = date_to_georgian(date.replace(year=year))
        self.update_calendars(date)

    def year_arrow_pressed(self, yera, icon_pos, event):
        if icon_pos == Gtk.EntryIconPosition.PRIMARY:
            date = add_years(self.parent.date, -1)
        else:
            date = add_years(self.parent.date, 1)
        self.update_calendars(date)

    def connect_month_combo(self, calendar):
        calendar.header.month.connect('changed',
                                      self.month_combo_changed, calendar.date)

    def month_combo_changed(self, combo, date):
        month = combo.get_active_id()
        date = date_to_georgian(date.replace(month=int(month)))
        self.update_calendars(date)

    def connect_month_arrow(self, calendar):
        # left arrow
        calendar.header.btl.connect("button-press-event",
                                    self.month_arrow_pressed, 'l')
        # right arrow
        calendar.header.btr.connect("button-press-event",
                                    self.month_arrow_pressed, 'r')

    def month_arrow_pressed(self, *args):
        l_r = args[-1]
        if l_r == 'r':
            date = add_months(self.parent.date, -1)
        else:
            date = add_months(self.parent.date, 1)
        self.update_calendars(date)

    def connect_date_buttons(self, calendar):
        button_list = calendar.grid.button_list
        for button, date, i, j in button_list:
            button.connect("button-press-event",
                           self.date_button_pressed, (i, j, date))

    def date_button_pressed(self, *args):
        date = date_to_georgian(args[-1][-1])
        self.update_calendars(date)

    def connect_month_buttons(self, months):
        button_list = months.grid.button_list
        for button, _, i in button_list:
            button.connect("button-press-event",
                           self.month_button_pressed, i, months.date)

    def month_button_pressed(self, *args):
        month, date = args[-2:]
        date = date.replace(month=month)
        date = date_to_georgian(date)
        self.update_calendars(date)


class MainWindow(Gtk.Window):

    def __init__(self, date=None):
        super().__init__(title='گاه شمار')
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)
        self.add(hbox)
        self.hbox = hbox
        if date is None:
            date = datetime.date.today()
        self.date = date

        self.vbox2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=250)
        pday = PersianDayWidget()
        gday = GeorgianDayWidget()
        self.vbox2.pack_start(gday, False, False, 0)
        self.vbox2.pack_start(pday, False, False, 0)
        self.day_widgets = [gday, pday]

        self.vbox3 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=200)
        pday = PersianMonthsWidget()
        gday = GeorgianMonthsWidget()
        self.vbox3.pack_start(gday, False, True, 0)
        self.vbox3.pack_start(pday, False, True, 0)
        self.months_widgets = [gday, pday]

        pcal = PersianCalendarWidget(khayyam.JalaliDate.from_date(date))
        gcal = GeorgianCalendarWidget(date)
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        self.vbox = vbox
        vbox.pack_start(gcal, False, False, 0)
        vbox.pack_start(pcal, False, False, 0)
        self.calendars = [gcal, pcal]
        self.handler = EventsHandler(self)
        # vbox.pack_start(Gtk.Calendar(), True, True, 0)
        self.hbox.pack_start(self.vbox2, False, False, 0)
        self.hbox.pack_start(self.vbox, False, False, 0)
        self.hbox.pack_start(self.vbox3, False, False, 0)

        # set header bar
        hb = Gtk.HeaderBar()
        hb.props.show_close_button = True
        hb.props.title = 'گاه شمار'
        button = Gtk.Button()
        icon = Gio.ThemedIcon(name="go-home")
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.LARGE_TOOLBAR)
        button.add(image)
        button.connect("clicked", self.set_today)
        hb.pack_start(button)
        self.set_titlebar(hb)

    def set_today(self, *args):
        self.handler.update_calendars(datetime.date.today())

if __name__ == '__main__':
    win = MainWindow()
    win.connect("delete-event", Gtk.main_quit)
    win.set_icon_name("calendar")
    win.show_all()
    Gtk.main()
