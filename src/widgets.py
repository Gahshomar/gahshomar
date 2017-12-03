# -*- Mode: Python; coding: utf-8; indent-tabs-mode: s; tab-width: 4 -*-

from gi.repository import Gtk
from .gi_composites import GtkTemplate


@GtkTemplate(ui='/org/gnome/Gahshomar/day-widget.ui')
class DayWidget(Gtk.Box):
    __gtype_name__ = 'DayWidget'

    label = GtkTemplate.Child()

    def __init__(self, date, **kwargs):
        super().__init__(**kwargs)
        self.init_template()
        self.date = date
        self.date.connect("notify::date", self.update)

    def __del__(self):
        self.date.disconnect_by_func(self.update)

    def update(self, date):
        self.label.set_markup(
            "<span size='large'>" + date.full_date + '</span>')


@GtkTemplate(ui='/org/gnome/Gahshomar/months-widget.ui')
class MonthsWidget(Gtk.Box):
    __gtype_name__ = 'MonthsWidget'

    grid = GtkTemplate.Child()
    button1 = GtkTemplate.Child()
    button2 = GtkTemplate.Child()
    button3 = GtkTemplate.Child()
    button4 = GtkTemplate.Child()
    button5 = GtkTemplate.Child()
    button6 = GtkTemplate.Child()
    button7 = GtkTemplate.Child()
    button8 = GtkTemplate.Child()
    button9 = GtkTemplate.Child()
    button10 = GtkTemplate.Child()
    button11 = GtkTemplate.Child()
    button12 = GtkTemplate.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.init_template()


@GtkTemplate(ui='/org/gnome/Gahshomar/calendar-widget.ui')
class CalendarWidget(Gtk.Box):
    __gtype_name__ = 'CalendarWidget'

    month_year_header = GtkTemplate.Child()
    months_button = GtkTemplate.Child()
    month_label = GtkTemplate.Child()
    popover = GtkTemplate.Child()
    year_entry = GtkTemplate.Child()
    week_days = GtkTemplate.Child()
    week_day1 = GtkTemplate.Child()
    week_day2 = GtkTemplate.Child()
    week_day3 = GtkTemplate.Child()
    week_day4 = GtkTemplate.Child()
    week_day5 = GtkTemplate.Child()
    week_day6 = GtkTemplate.Child()
    week_day7 = GtkTemplate.Child()
    days_grid = GtkTemplate.Child()
    button1 = GtkTemplate.Child()
    button2 = GtkTemplate.Child()
    button3 = GtkTemplate.Child()
    button4 = GtkTemplate.Child()
    button5 = GtkTemplate.Child()
    button6 = GtkTemplate.Child()
    button7 = GtkTemplate.Child()
    button8 = GtkTemplate.Child()
    button9 = GtkTemplate.Child()
    button10 = GtkTemplate.Child()
    button11 = GtkTemplate.Child()
    button12 = GtkTemplate.Child()
    button13 = GtkTemplate.Child()
    button14 = GtkTemplate.Child()
    button15 = GtkTemplate.Child()
    button16 = GtkTemplate.Child()
    button17 = GtkTemplate.Child()
    button18 = GtkTemplate.Child()
    button19 = GtkTemplate.Child()
    button20 = GtkTemplate.Child()
    button21 = GtkTemplate.Child()
    button22 = GtkTemplate.Child()
    button23 = GtkTemplate.Child()
    button24 = GtkTemplate.Child()
    button25 = GtkTemplate.Child()
    button26 = GtkTemplate.Child()
    button27 = GtkTemplate.Child()
    button28 = GtkTemplate.Child()
    button29 = GtkTemplate.Child()
    button30 = GtkTemplate.Child()
    button31 = GtkTemplate.Child()
    button32 = GtkTemplate.Child()
    button33 = GtkTemplate.Child()
    button34 = GtkTemplate.Child()
    button35 = GtkTemplate.Child()
    button36 = GtkTemplate.Child()
    button37 = GtkTemplate.Child()
    button38 = GtkTemplate.Child()
    button39 = GtkTemplate.Child()
    button40 = GtkTemplate.Child()
    button41 = GtkTemplate.Child()
    button42 = GtkTemplate.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.init_template()

    # @log
    # def update(self, date=None, **kwargs):
    #     if date is None:
    #         date = self.date
    #     self.date = self.get_date(date)

    #     month_label = self.get_months()[self.date.month - 1]
    #     self.MonthLabel.set_label(month_label)

    #     self.YearEntry.set_text(calendar.glib_strftime(_('%Y'), self.date))

    #     self.setup_weekdays()

    #     self.show_all()
    #     self.setup_days_grid()

    # @log
    # def setup_days_grid(self):
    #     self.gen_grid_mat()
    #     for button, __ in self.days_button_list:
    #         button.hide()
    #     for j, row in enumerate(self.grid_mat):
    #         for i, (date, day) in enumerate(row):
    #             if date.month == self.date.month:
    #                 text = '<span fgcolor="black">{}</span>'
    #             else:
    #                 text = '<span fgcolor="gray">{}</span>'
    #             text = text.format(day)
    #             button, sig_id = self.days_button_list[j * 7 + i]
    #             label = Gtk.Label()
    #             label.set_markup(text)
    #             button.set_label('')
    #             button.set_always_show_image(True)
    #             button.set_image(label)
    #             button.set_relief(Gtk.ReliefStyle.NONE)
    #             if date == self.date:
    #                 button.set_relief(Gtk.ReliefStyle.HALF)
    #             if sig_id is not None:
    #                 button.disconnect(sig_id)
    #             sig_id = button.connect("clicked",
    #                                     self.date_button_pressed, (i, j, date))
    #             self.days_button_list[j * 7 + i][1] = sig_id
    #             button.show()

    # @log
    # def setup_weekdays(self):
    #     for i, (week_day, tooltip) in enumerate(self.week_days):
    #         if self.rtl:
    #             j = i + 1
    #         else:
    #             j = i + 1
    #         label = self.ui.get_object('WeekDay{}'.format(j))
    #         label.set_markup(
    #             "<span foreground='#4A90D9'>" +  # background='#4A90D9'
    #             week_day + '</span>')
    #         label.set_tooltip_markup(tooltip)

    # @log
    # def date_button_pressed(self, *args):
    #     date = args[-1][-1]
    #     self.app.handler.update_everything(date=date)

    # @log
    # def year_entered(self, yearEntry):
    #     year = yearEntry.get_text()
    #     try:
    #         year = int(year)
    #         self.date = self.date.replace(year=year)
    #     except Exception:
    #         logger.exception(Exception)
    #     self.app.handler.update_everything(date=self.date)

    # @log
    # def year_arrow_pressed(self, year_entry, icon_pos, event):
    #     if icon_pos == Gtk.EntryIconPosition.PRIMARY:
    #         date = add_years(self.date, -1)
    #     else:
    #         date = add_years(self.date, 1)
    #     self.app.handler.update_everything(date=date)

    # @log
    # def display_months(self, *args):
    #     if self.MonthMenuButton is not None:
    #         if self.MonthMenuButton.get_active():
    #             self.popover.show_all()
    #         else:
    #             self.popover.hide()
    #     else:
    #         self.popover.show_all()
