#!/usr/bin/env python3
# -*- Mode: Python; coding: utf-8; indent-tabs-mode: s; tab-width: 4 -*-
#
# Copyright (C) 2014 Amir Mohammadi <183.amir@gmail.com>
#
# Gahshomar is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Gahshomar is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.


class EventsHandler(object):
    """docstring for EventsHandler"""
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

    def update_everything(self, date=None):
        if date is None:
            date = self.parent.date
        self.parent.date = date
        if self.parent.visible:
            self.update_calendars(date)
            self.update_day_widgets(date)
            self.parent.draw_interface()
            self.parent.show_all()
        self.update_appindicator()

    def update_calendars(self, date):
        '''update calendars'''
        for calendar in self.parent.calendars:
            calendar.destroy()
            calendar.__init__(date)

    def update_day_widgets(self, date):
        for dayw in self.parent.day_widgets:
            dayw.destroy()
            dayw.__init__(date)

    def update_appindicator(self):
        self.parent.ind.update()
