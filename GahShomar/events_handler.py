#!/usr/bin/env python3


class EventsHandler(object):
    """docstring for EventsHandler"""
    def __init__(self, parent):
        super().__init__()
        self.calendars = parent.calendars
        self.parent = parent

    def update_everything(self, date):
        self.parent.date = date
        self.update_calendars(date)
        self.update_day_widgets(date)
        self.parent.draw_interface()
        self.parent.show_all()

    def update_calendars(self, date):
        '''update calendars'''
        for calendar in self.calendars:
            calendar.destroy()
            calendar.__init__(date)

    def update_day_widgets(self, date):
        for dayw in self.parent.day_widgets:
            dayw.destroy()
            dayw.__init__(date)


