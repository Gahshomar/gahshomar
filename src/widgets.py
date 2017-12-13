# -*- Mode: Python; coding: utf-8; indent-tabs-mode: s; tab-width: 4 -*-

from gi.repository import Gtk
from .gi_composites import GtkTemplate
import logging
logger = logging.getLogger(__name__)


@GtkTemplate(ui='/org/gahshomar/Gahshomar/day-widget.ui')
class DayWidget(Gtk.Box):
    __gtype_name__ = 'DayWidget'

    label = GtkTemplate.Child()

    def __init__(self, calendar, **kwargs):
        super().__init__(**kwargs)
        self.init_template()
        self.calendar = calendar
        self.calendar.connect("notify::date", self.update)
        self.calendar.connect("notify::date-format", self.update)
        self.update(self.calendar)

    def __del__(self):
        self.calendar.disconnect_by_func(self.update)

    def update(self, calendar, *args):
        logger.debug('DayWidget is updating %s', args)
        self.label.set_markup(
            "<span size='large'>" + calendar.full_date + '</span>')


@GtkTemplate(ui='/org/gahshomar/Gahshomar/months-widget.ui')
class MonthsWidget(Gtk.Box):
    __gtype_name__ = 'MonthsWidget'

    grid = GtkTemplate.Child()

    def __init__(self, ref_calendar, calendar, **kwargs):
        super().__init__(**kwargs)
        self.init_template()
        self.ref_calendar = ref_calendar
        self.calendar = calendar
        self.button_list = self.grid.get_children()[::-1]
        self.calendar.connect("notify::date", self.update)
        self.calendar.connect("notify::date-format", self.update)
        self.update(self.calendar)

    def __del__(self):
        self.calendar.disconnect_by_func(self.update)

    def update(self, calendar, *args):
        month_list = []
        for i, month in enumerate(calendar.months):
            if calendar.rtl:
                if i % 3 == 0:
                    j = i + 2
                elif i % 3 == 1:
                    j = i
                else:
                    j = i - 2
            else:
                j = i
            button = self.button_list[j]
            month_list.append((button, month, i + 1))
            try:
                button.disconnect_by_func(self.month_button_pressed)
            except TypeError:
                pass
            button.connect("clicked", self.month_button_pressed, i + 1)
        for button, month, i in month_list:
            button.set_label(month)
            if i == calendar.month:
                button.set_relief(Gtk.ReliefStyle.HALF)
                self.grid.set_focus_child(button)
            else:
                button.set_relief(Gtk.ReliefStyle.NONE)

    def month_button_pressed(self, *args):
        month = args[-1]
        self.ref_calendar.date = self.calendar.add_months(
            month - self.calendar.month)


@GtkTemplate(ui='/org/gahshomar/Gahshomar/calendar-widget.ui')
class CalendarWidget(Gtk.Box):
    __gtype_name__ = 'CalendarWidget'

    month_year_header = GtkTemplate.Child()
    months_button = GtkTemplate.Child()
    month_label = GtkTemplate.Child()
    popover = GtkTemplate.Child()
    year_entry = GtkTemplate.Child()
    week_days = GtkTemplate.Child()
    days_grid = GtkTemplate.Child()

    def __init__(self, ref_calendar, calendar, **kwargs):
        super().__init__(**kwargs)
        self.init_template()
        self.days_buttons = self.days_grid.get_children()[::-1]
        self.week_labels = self.week_days.get_children()
        self.ref_calendar = ref_calendar
        self.calendar = calendar
        self.calendar.connect("notify::date", self.update)
        self.calendar.connect("notify::date-format", self.update)
        self.update(self.calendar)

    def __del__(self):
        self.calendar.disconnect_by_func(self.update)

    def update(self, calendar, *args):

        month_label = calendar.months[self.calendar.month - 1]
        self.month_label.set_label(month_label)
        self.year_entry.set_text(calendar.strftime('%Y'))
        self.setup_weekdays()
        self.setup_days_grid()

    def setup_days_grid(self):
        # hide buttons since they might not be needed.
        for button in self.days_buttons:
            button.hide()
        for j, row in enumerate(self.calendar.grid_mat):
            for i, (date, day) in enumerate(row):
                if date.month == self.calendar.month:
                    text = '<span fgcolor="black">{}</span>'
                else:
                    text = '<span fgcolor="gray">{}</span>'
                text = text.format(day)
                button = self.days_buttons[j * 7 + i]
                label = Gtk.Label()
                label.set_markup(text)
                button.set_label('')
                button.set_always_show_image(True)
                button.set_image(label)
                button.set_relief(Gtk.ReliefStyle.NONE)
                if date == self.calendar.date:
                    button.set_relief(Gtk.ReliefStyle.HALF)
                try:
                    button.disconnect_by_func(self.date_button_pressed)
                except TypeError:
                    pass
                button.connect("clicked",
                               self.date_button_pressed,
                               (i, j, date))
                button.show()

    def setup_weekdays(self):
        week_days = self.calendar.week_days
        if self.calendar.rtl:
            week_days = week_days[::-1]
        for i, (week_day, tooltip) in enumerate(week_days):
            label = self.week_labels[i]
            label.set_markup("<span foreground='#4A90D9'>" + week_day +
                             '</span>')
            label.set_tooltip_markup(tooltip)

    def date_button_pressed(self, *args):
        self.ref_calendar.date = args[-1][-1]

    @GtkTemplate.Callback
    def on_year_entry_activate(self, year_entry, *args):
        year = year_entry.get_text()
        try:
            year = int(year)
            date = self.calendar.replace(year=year)
        except Exception:
            pass
        self.ref_calendar.date = date

    @GtkTemplate.Callback
    def on_year_entry_icon_press(self, year_entry, icon_pos, event, *args):
        if icon_pos == Gtk.EntryIconPosition.PRIMARY:
            date = self.calendar.add_years(-1)
        else:
            date = self.calendar.add_years(1)
        self.ref_calendar.date = date
